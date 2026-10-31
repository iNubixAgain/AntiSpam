"""Comprueba conexión, permisos, consultas y botones sin insertar datos."""

import argparse
import asyncio
import sys
from urllib.request import urlopen

from utilidades import RAIZ

sys.path.insert(0, str(RAIZ))

from analisis import analizar_mensaje
from base_datos import conectar, estadisticas


def comprobar(condicion, mensaje):
    if not condicion:
        raise RuntimeError(mensaje)


def probar(http=False):
    with conectar() as con:
        comprobar(con.read_only, "La conexión no está en modo de solo lectura.")
        for tabla in ("fuentes", "mensajes"):
            for permiso in ("INSERT", "UPDATE", "DELETE", "TRUNCATE"):
                permitido = con.execute(
                    "SELECT has_table_privilege(current_user,%s,%s) AS permitido",
                    (tabla, permiso),
                ).fetchone()["permitido"]
                comprobar(not permitido, f"La cuenta tiene {permiso} sobre {tabla}.")
        totales = estadisticas(con)
        total = sum(f["total"] for f in totales)
        fila = con.execute("SELECT contenido,canal FROM mensajes ORDER BY id LIMIT 1").fetchone()
    print(f"PostgreSQL: conectado, solo lectura; {total} registros.")
    for fuente in totales:
        print(f"  {fuente['codigo']}: {fuente['total']}")
    if fila:
        resultado = analizar_mensaje(fila["contenido"], fila["canal"])
        comprobar(resultado[4] in ("Etiqueta original", "Sin clasificación"), "Falló la consulta de un registro existente.")
        comprobar(resultado[2] != "PostgreSQL no disponible.", "Falló la consulta de etiquetas.")
    comprobar(analizar_mensaje("", "SMS")[0] == "Sin analizar", "Falló la validación del mensaje vacío.")

    from app import demo, limpiar

    comprobar(limpiar() == ("", "SMS", "", "", "", "", ""), "Falló Limpiar.")

    comprobar(len(demo.config["dependencies"]) == 2, "La interfaz debe tener solo Analizar y Limpiar.")
    comprobar(not any(c["type"] in ("tabitem", "dataframe", "dropdown") for c in demo.config["components"]), "La interfaz no debe mostrar datasets.")

    async def botones():
        analisis = await demo.process_api(0, ["", "SMS"], state=None)
        comprobar(analisis["data"][0] == "Sin analizar", "Falló el botón Analizar mensaje.")
        limpio = await demo.process_api(1, [], state=None)
        comprobar(limpio["data"] == ["", "SMS", "", "", "", "", ""], "Falló el botón Limpiar.")

    asyncio.run(botones())
    with conectar() as con:
        comprobar(sum(f["total"] for f in estadisticas(con)) == total, "Cambió el total de registros durante la comprobación.")
    print("Consultas y botones: correctos; no se escribieron registros.")
    if http:
        with urlopen("http://127.0.0.1:7860/", timeout=5) as respuesta:
            comprobar(respuesta.status == 200, "Gradio no respondió correctamente.")
        print("Gradio HTTP: disponible en http://127.0.0.1:7860.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--http", action="store_true", help="Verifica además Gradio, que debe estar ejecutándose.")
    args = parser.parse_args()
    try:
        probar(args.http)
    except RuntimeError as error:
        parser.exit(1, str(error) + "\n")
    except Exception as error:
        parser.exit(1, f"Comprobación fallida ({type(error).__name__}). Revisa PostgreSQL, .env y la aplicación.\n")
