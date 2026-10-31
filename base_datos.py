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


def explorar(fuente="Todas", etiqueta="Todas", busqueda="", pagina=1):
    pagina = max(1, int(pagina))
    with conectar() as con:
        resumen = estadisticas(con)
        filas = con.execute(
            """SELECT m.id,f.codigo,m.canal,m.etiqueta_original,
            CASE WHEN f.codigo='enron' THEN '[Contenido privado: no se muestra]'
            ELSE left(m.contenido,240) END AS ejemplo
            FROM mensajes m JOIN fuentes f ON f.id=m.fuente_id
            WHERE (%s='Todas' OR f.codigo=%s)
            AND (%s='Todas' OR (%s='Sin etiqueta' AND m.etiqueta_original IS NULL)
                 OR m.etiqueta_original=%s)
            AND (%s='' OR (f.codigo<>'enron' AND position(lower(%s) IN lower(m.contenido))>0))
            ORDER BY m.id LIMIT 10 OFFSET %s""",
            (fuente, fuente, etiqueta, etiqueta, etiqueta, busqueda, busqueda, (pagina - 1) * 10),
        ).fetchall()
    return resumen, filas
