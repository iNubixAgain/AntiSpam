"""Configuración compartida de las herramientas, independiente de Gradio."""

import os
from pathlib import Path

from dotenv import load_dotenv
from psycopg.conninfo import conninfo_to_dict, make_conninfo

RAIZ = Path(__file__).resolve().parent.parent


def ruta_proyecto(nombre):
    ruta = Path(nombre)
    return ruta if ruta.is_absolute() else RAIZ / ruta


def conexion_configurada(variable):
    load_dotenv(RAIZ / ".env", encoding="utf-8-sig")
    valor = os.getenv(variable)
    if not valor:
        raise RuntimeError(f"Configura {variable} en .env o en la terminal.")
    return valor


def argumentos_conexion(url):
    """Conserva las opciones libpq y separa la contraseña de los argumentos."""
    parametros = conninfo_to_dict(url)
    entorno = os.environ.copy()
    entorno.pop("PGPASSWORD", None)
    clave = parametros.pop("password", None)
    if clave is not None:
        entorno["PGPASSWORD"] = clave
    return make_conninfo(**parametros), entorno
