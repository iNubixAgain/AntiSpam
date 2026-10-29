
import gradio as gr


# Función provisional: todavía NO utiliza inteligencia artificial.
def analizar_mensaje(mensaje, canal):

    if not mensaje or not mensaje.strip():
        return (
            "Sin analizar",
            "Sin determinar",
            "No hay indicadores.",
            "Escribe o pega un mensaje antes de analizarlo."
        )

    texto = mensaje.lower()

    senales_fraude = [
        "verifica tu cuenta",
        "contraseña",
        "datos bancarios",
        "cuenta será bloqueada",
        "transferencia urgente"
    ]

    senales_spam = [
        "oferta",
        "descuento",
        "promoción",
        "premio",
        "gratis"
    ]

    encontradas_fraude = [
        palabra for palabra in senales_fraude if palabra in texto
    ]

    encontradas_spam = [
        palabra for palabra in senales_spam if palabra in texto
    ]

    tiene_enlace = any(
        marca in texto
        for marca in ["https://", "http://", "www."]
    )

    if encontradas_fraude:
        clase = "Potencialmente fraudulento"
        riesgo = "Alto (simulado)"
        senales = encontradas_fraude
        consejo = (
            "No compartas contraseñas ni datos bancarios. "
            "Verifica el aviso mediante un canal oficial."
        )

    elif encontradas_spam:
        clase = "Spam"
        riesgo = "Medio (simulado)"
        senales = encontradas_spam
        consejo = (
            "Evita responder a mensajes publicitarios "
            "inesperados o abrir sus enlaces."
        )

    else:
        clase = "Normal (provisional)"
        riesgo = "Bajo (simulado)"
        senales = []
        consejo = (
            "No se encontraron las expresiones del prototipo. "
            "Aun así, verifica el remitente."
        )

    if tiene_enlace:
        senales.append("contiene un enlace")
        consejo += " No abras enlaces si no conoces su origen."

    indicadores = (
        ", ".join(senales)
        if senales
        else "No se detectaron indicadores de ejemplo."
    )

    return clase, riesgo, indicadores, consejo


# Restablece los campos de la interfaz.
def limpiar():
    return "", "SMS", "", "", "", ""


# Construcción de la interfaz.
with gr.Blocks(
    title="Detector de spam",
    analytics_enabled=False
) as demo:

    gr.Markdown("# Detector de spam y mensajes fraudulentos")
    gr.Markdown(
        "Prototipo académico: utiliza reglas de ejemplo, "
        "no un modelo de IA entrenado."
    )

    with gr.Row():

        # Sección de entrada.
        with gr.Column():

            mensaje = gr.Textbox(
                label="Mensaje que deseas revisar",
                placeholder="Escribe o pega aquí un mensaje...",
                lines=8
            )

            canal = gr.Radio(
                ["SMS", "Correo", "Chat"],
                value="SMS",
                label="Canal del mensaje"
            )

            with gr.Row():
                boton_analizar = gr.Button(
                    "Analizar mensaje",
                    variant="primary"
                )
                boton_limpiar = gr.Button("Limpiar")

        # Sección de resultados.
        with gr.Column():

            clasificacion = gr.Textbox(
                label="Clasificación",
                interactive=False
            )

            riesgo = gr.Textbox(
                label="Nivel de riesgo",
                interactive=False
            )

            indicadores = gr.Textbox(
                label="Indicadores detectados",
                lines=3,
                interactive=False
            )

            recomendacion = gr.Textbox(
                label="Recomendación",
                lines=3,
                interactive=False
            )

    gr.Markdown(
        "**Aviso:** los resultados son simulados y no "
        "garantizan que un mensaje sea seguro."
    )

    # Vinculamos los botones a sus funciones.
    boton_analizar.click(
        fn=analizar_mensaje,
        inputs=[mensaje, canal],
        outputs=[
            clasificacion,
            riesgo,
            indicadores,
            recomendacion
        ]
    )

    boton_limpiar.click(
        fn=limpiar,
        inputs=[],
        outputs=[
            mensaje,
            canal,
            clasificacion,
            riesgo,
            indicadores,
            recomendacion
        ]
    )


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        share=False
    )
