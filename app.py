"""Interfaz local; no guarda mensajes de los usuarios."""

import re

import gradio as gr
import psycopg

import base_datos as db
from analisis import analizar_mensaje


def limpiar():
    return "", "SMS", "", "", "", "", ""


def ocultar(texto):
    texto = re.sub(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", "[correo oculto]", texto)
    texto = re.sub(r"(?:https?://|www\.)\S+", "[enlace oculto]", texto)
    return re.sub(r"\+?\d[\d ()-]{6,}\d", "[número oculto]", texto)


def consultar_datasets(fuente, etiqueta, busqueda, pagina):
    try:
        resumen, filas = db.explorar(fuente, etiqueta, busqueda, int(pagina))
        return (
            "PostgreSQL conectado en modo de solo lectura. Diez resultados por página.",
            [list(r.values()) for r in resumen],
            [
                [
                    r["id"],
                    r["codigo"],
                    r["canal"],
                    r["etiqueta_original"] or "Sin etiqueta",
                    ocultar(r["ejemplo"]),
                ]
                for r in filas
            ],
        )
    except (psycopg.Error, RuntimeError, ValueError, OverflowError):
        return (
            "Sin conexión. Revisa DATABASE_URL e inicia PostgreSQL con iniciar_postgresql.ps1.",
            [],
            [],
        )


with gr.Blocks(title="Detector de spam", analytics_enabled=False) as demo:
    gr.Markdown("# Detector de spam y mensajes potencialmente fraudulentos")
    gr.Markdown(
        "Proyecto 5 · Fundamentos de Inteligencia Artificial. Solo consulta etiquetas originales de los registros existentes. Sin predicciones ni inserción de datos. No introduzcas información sensible."
    )
    with gr.Tab("Revisar un mensaje"):
        with gr.Row():
            with gr.Column():
                mensaje = gr.Textbox(
                    label="Mensaje que deseas revisar", lines=10, max_length=100000
                )
                canal = gr.Radio(
                    ["SMS", "Correo", "Chat"], value="SMS", label="¿Cómo recibiste el mensaje?"
                )
                with gr.Row():
                    boton_analizar = gr.Button("Analizar mensaje", variant="primary")
                    boton_limpiar = gr.Button("Limpiar")
            with gr.Column():
                clasificacion = gr.Textbox(label="Clasificación", interactive=False)
                riesgo = gr.Textbox(label="Nivel de riesgo", interactive=False)
                indicadores = gr.Textbox(
                    label="Indicadores o procedencia", lines=4, interactive=False
                )
                recomendacion = gr.Textbox(label="Recomendación", lines=5, interactive=False)
                metodo = gr.Textbox(label="Método utilizado", interactive=False)
        salidas = [clasificacion, riesgo, indicadores, recomendacion, metodo]
        boton_analizar.click(analizar_mensaje, [mensaje, canal], salidas, api_name=False)
        boton_limpiar.click(limpiar, [], [mensaje, canal, *salidas], api_name=False)
    with gr.Tab("Explorar datasets"):
        gr.Markdown(
            "La consulta se realiza al pulsar Buscar. Enron muestra solo metadatos. Las otras vistas ocultan correos, números y enlaces, pero pueden contener nombres: evita redistribuir ejemplos."
        )
        fuente = gr.Dropdown(
            ["Todas", "uci", "spamassassin", "enron"], value="Todas", label="Dataset"
        )
        etiqueta = gr.Dropdown(
            ["Todas", "ham", "spam", "Sin etiqueta"], value="Todas", label="Clasificación original"
        )
        busqueda = gr.Textbox(
            label="Buscar texto (no disponible en contenido de Enron)", max_length=200
        )
        pagina = gr.Number(value=1, minimum=1, precision=0, label="Página (10 ejemplos)")
        buscar = gr.Button("Buscar / actualizar estado")
        estado = gr.Textbox(label="Estado de PostgreSQL", interactive=False)
        totales = gr.Dataframe(
            headers=["Fuente", "Total", "ham", "spam", "Sin etiqueta"], interactive=False
        )
        ejemplos = gr.Dataframe(
            headers=["ID", "Fuente", "Canal", "Etiqueta original", "Ejemplo limitado"],
            interactive=False,
        )
        buscar.click(
            consultar_datasets,
            [fuente, etiqueta, busqueda, pagina],
            [estado, totales, ejemplos],
            api_name=False,
        )
    gr.Markdown(
        "Una etiqueta original no garantiza seguridad. Los mensajes nuevos no se clasifican ni se guardan. La aplicación tiene únicamente permisos de lectura."
    )


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", share=False)
