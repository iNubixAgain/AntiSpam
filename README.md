# AntiSpam

Detector académico con Python, Gradio y PostgreSQL, de la materia Fundamentos de Inteligencia Artificial.

Consulta exclusivamente etiquetas originales de los mensajes existentes en la base de datos. No inserta registros, no entrena modelos y no clasifica mensajes nuevos.

- [Instalación y ejecución](Documentacion/GUIA_INSTALACION.md)
- [Arquitectura, fuentes y privacidad](Documentacion/DOCUMENTACION.md)
- [Importar, exportar y comprobar la app](tools/GUIA_TOOLS.md)

La interfaz permite introducir un mensaje, seleccionar su canal y consultar su clasificación. Utiliza internamente los datos de UCI y SpamAssassin, sin mostrar los datasets en la página. Si no hay una etiqueta original disponible, informa que el mensaje está sin clasificación.

Para empezar, consulta la guía de instalación. Cada integrante necesita Python, PostgreSQL y su propia configuración. El repositorio incluye el [respaldo completo](Documentacion/antispam-completo.dump) y un [TXT con los mensajes para probar](Documentacion/ejemplos-antispam-completo.txt), con su fuente, canal y etiqueta original. Son mensajes reales: revisa las condiciones de uso y privacidad descritas en la documentación antes de redistribuirlos.
