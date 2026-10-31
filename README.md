# AntiSpam

Detector académico con Python, Gradio y PostgreSQL, de la materia Fundamentos de Inteligencia Artificial.

Consulta exclusivamente etiquetas originales de los mensajes existentes en la base de datos. No inserta registros, no entrena modelos y no clasifica mensajes nuevos.

- [Instalación y ejecución](Documentacion/GUIA_INSTALACION.md)
- [Arquitectura, fuentes y privacidad](Documentacion/DOCUMENTACION.md)
- [Importar, exportar y comprobar la app](tools/GUIA_TOOLS.md)

La interfaz permite introducir un mensaje, seleccionar su canal y consultar su clasificación. Utiliza internamente los datos de UCI y SpamAssassin, sin mostrar los datasets en la página. Si no hay una etiqueta original disponible, informa que el mensaje está sin clasificación.

Para empezar, consulta la guía de instalación. Cada integrante necesita Python, PostgreSQL, su propia configuración y una copia de la base. Los dumps son locales y se comparten por separado; no se publican en GitHub.
