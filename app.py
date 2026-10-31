"""Interfaz local; no guarda mensajes de los usuarios."""

import gradio as gr
from analisis import analizar_mensaje


def limpiar():
    return "", "SMS", "", "", "", "", ""


with gr.Blocks(title="Detector de spam", analytics_enabled=False) as demo:
    gr.Markdown("# Detector de spam y mensajes potencialmente fraudulentos")
    gr.Markdown(
        "Proyecto 5 · Fundamentos de Inteligencia Artificial. Solo consulta etiquetas originales de los registros existentes. Sin predicciones ni inserción de datos. No introduzcas información sensible."
    )
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
    gr.Markdown(
        "Una etiqueta original no garantiza seguridad. Los mensajes nuevos no se clasifican ni se guardan. La aplicación tiene únicamente permisos de lectura."
    )


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", share=False)
