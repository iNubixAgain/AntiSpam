"""Exporta la base completa con pg_dump, sin modificarla ni sobrescribir archivos."""

import argparse
import subprocess

from utilidades import argumentos_conexion, conexion_configurada, ruta_proyecto


def respaldar(destino, ejecutable="pg_dump"):
    conexion, entorno = argumentos_conexion(conexion_configurada("DATABASE_URL"))
    ruta = ruta_proyecto(destino)
    with ruta.open("xb") as salida:
        try:
            proceso = subprocess.run(
                [ejecutable, "--dbname", conexion, "--format=custom", "--no-owner"],
                stdout=salida, stderr=subprocess.PIPE, env=entorno,
            )
            if proceso.returncode:
                raise RuntimeError("pg_dump falló. Revisa conexión, permisos y versión del cliente.")
        except Exception:
            salida.close()
            ruta.unlink(missing_ok=True)
            raise
    return ruta


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destino", help="Ruta relativa a la raíz del proyecto.")
    parser.add_argument("--pg-dump", default="pg_dump", help="Ejecutable oficial en PATH.")
    args = parser.parse_args()
    try:
        respaldar(args.destino, args.pg_dump)
    except FileExistsError:
        parser.exit(1, "El respaldo ya existe. Elige otro nombre; no se sobrescribió.\n")
    except Exception as error:
        parser.exit(1, f"No se pudo crear el respaldo ({type(error).__name__}). Revisa configuración, carpeta de destino y pg_dump.\n")
    print("Respaldo completo creado con pg_dump.")
