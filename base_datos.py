"""Acceso exclusivo a PostgreSQL; ninguna consulta de usuario escribe registros."""

import hashlib
import os
import unicodedata

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv(encoding="utf-8-sig")


def normalizar(texto):
    return " ".join(unicodedata.normalize("NFKC", texto).casefold().split())


def huella(texto):
    return hashlib.sha256(normalizar(texto).encode("utf-8")).hexdigest()


def conectar(url=None):
    destino = url or os.getenv("DATABASE_URL")
    if not destino:
        raise RuntimeError("Configura DATABASE_URL en .env.")
    con = psycopg.connect(destino, row_factory=dict_row, connect_timeout=3)
    con.read_only = True
    return con


def buscar_exactos(texto, canal):
    with conectar() as con:
        return con.execute(
            """SELECT f.codigo,f.nombre,m.canal,m.etiqueta_original,
            count(*) AS cantidad FROM mensajes m JOIN fuentes f ON f.id=m.fuente_id
            WHERE m.canal=%s AND m.hash_contenido=%s AND m.texto_normalizado=%s
            GROUP BY f.codigo,f.nombre,m.canal,m.etiqueta_original""",
            (canal, huella(texto), normalizar(texto)),
        ).fetchall()


def estadisticas(con):
    return con.execute("""SELECT f.codigo, count(m.id) AS total,
        count(m.id) FILTER (WHERE m.etiqueta_original='ham') AS ham,
        count(m.id) FILTER (WHERE m.etiqueta_original='spam') AS spam,
        count(m.id) FILTER (WHERE m.etiqueta_original IS NULL) AS sin_etiqueta
        FROM fuentes f LEFT JOIN mensajes m ON m.fuente_id=f.id GROUP BY f.codigo ORDER BY f.codigo""").fetchall()
