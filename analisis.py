"""Consulta exclusiva de etiquetas existentes; sin predicción ni escritura."""

import psycopg

import base_datos as db


def analizar_mensaje(mensaje, canal):
    if not mensaje or not mensaje.strip():
        return (
            "Sin analizar",
            "Sin determinar",
            "No hay indicadores.",
            "Escribe o pega un mensaje antes de analizarlo.",
            "Sin clasificación",
        )
    if canal not in ("SMS", "Correo", "Chat"):
        return (
            "Sin analizar",
            "Sin determinar",
            "Canal inválido.",
            "Selecciona SMS, Correo o Chat.",
            "Sin clasificación",
        )
    try:
        registros = db.buscar_exactos(mensaje, canal)
    except (psycopg.Error, RuntimeError):
        return (
            "Sin clasificación",
            "Sin determinar",
            "PostgreSQL no disponible.",
            "No se pudo consultar la base de datos. Inténtalo más tarde.",
            "Sin clasificación",
        )
    etiquetas = {r["etiqueta_original"] for r in registros if r["etiqueta_original"]}
    procedencia = "; ".join(
        f"{r['nombre']} ({r['canal']}): {r['etiqueta_original'] or 'sin clasificación original'}"
        for r in registros
    )
    if len(etiquetas) == 1:
        etiqueta = next(iter(etiquetas))
        return (
            f"{etiqueta} (etiqueta original)",
            "No inferido de la etiqueta",
            procedencia,
            "Consulta de una etiqueta existente, no es una predicción ni garantiza seguridad.",
            "Etiqueta original",
        )
    if len(etiquetas) > 1:
        aviso = (
            "Hay etiquetas originales contradictorias: "
            + procedencia
            + ". No se asigna una clasificación."
        )
    elif registros:
        aviso = "Registro encontrado sin clasificación original: " + procedencia + "."
    else:
        aviso = "No se encontró el mensaje en los datasets del canal seleccionado."
    return (
        "Sin clasificación",
        "Sin determinar",
        procedencia or "Sin coincidencias.",
        aviso + " Solo se consultan registros existentes; no se guarda el mensaje.",
        "Sin clasificación",
    )
