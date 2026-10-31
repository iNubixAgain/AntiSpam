"""Restaura un dump de confianza solo en una base nueva y vacía, con pg_restore."""

import argparse
import subprocess

import psycopg

from utilidades import argumentos_conexion, conexion_configurada, ruta_proyecto


def restaurar(archivo, ejecutable="pg_restore"):
    ruta = ruta_proyecto(archivo)
    if not ruta.is_file():
        raise RuntimeError("No se encontró el dump local.")
    url = conexion_configurada("RESTORE_DATABASE_URL")
    with psycopg.connect(url, connect_timeout=5) as con:
        base = con.execute("SELECT current_database()").fetchone()[0]
        if base in ("postgres", "template0", "template1"):
            raise RuntimeError("No se restaura sobre bases de mantenimiento.")
        objetos = con.execute("""
            SELECT EXISTS (
                SELECT 1 FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
                WHERE n.nspname NOT LIKE 'pg_%' AND n.nspname <> 'information_schema'
            ) OR EXISTS (
                SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
                WHERE n.nspname NOT LIKE 'pg_%' AND n.nspname <> 'information_schema'
            )
        """).fetchone()[0]
        if objetos:
            raise RuntimeError("La base destino contiene objetos. Usa una base nueva y vacía.")
    conexion, entorno = argumentos_conexion(url)
    proceso = subprocess.run(
        [ejecutable, "--dbname", conexion, "--single-transaction", "--exit-on-error",
         "--no-owner", "--no-privileges", str(ruta)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=entorno,
    )
    if proceso.returncode:
        raise RuntimeError("pg_restore falló; la transacción fue revertida. Revisa el archivo y los permisos.")
    with psycopg.connect(url, connect_timeout=5) as con:
        fuentes = con.execute("SELECT count(*) FROM public.fuentes").fetchone()[0]
        mensajes = con.execute("SELECT count(*) FROM public.mensajes").fetchone()[0]
    return fuentes, mensajes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archivo", nargs="?", default="Documentacion/antispam-completo.dump",
                        help="Dump local relativo a la raíz del proyecto.")
    parser.add_argument("--pg-restore", default="pg_restore", help="Ejecutable oficial en PATH.")
    args = parser.parse_args()
    try:
        fuentes, mensajes = restaurar(args.archivo, args.pg_restore)
    except RuntimeError as error:
        parser.exit(1, str(error) + "\n")
    except Exception as error:
        parser.exit(1, f"No se pudo restaurar ({type(error).__name__}). Revisa RESTORE_DATABASE_URL, el archivo y pg_restore.\n")
    print(f"Restauración verificada: {fuentes} fuentes y {mensajes} mensajes.")
    print("Configura una cuenta de solo lectura en DATABASE_URL antes de abrir la aplicación.")
