# AntiSpam

Detector académico con Python, Gradio y PostgreSQL, de la materia Fundamentos de Inteligencia Artificial.

Consulta exclusivamente etiquetas originales de los mensajes existentes en la base de datos. No inserta registros, no entrena modelos y no clasifica mensajes nuevos.

- [Instalación, ejecución y respaldo](../README.md)
- [Arquitectura, fuentes y privacidad](../Documentacion/DOCUMENTACION.md)
- [Importar, exportar y comprobar la app](../tools/GUIA_TOOLS.md)

El README principal está en la raíz y la documentación técnica permanece en `Documentacion/`. Los dumps solo están disponibles localmente y no se publican en GitHub. Un clon no incluye datos reales, credenciales ni la instancia PostgreSQL local.

Con las dependencias y la conexión PostgreSQL configuradas, ejecute desde la raíz del proyecto (la carpeta que contiene `app.py`):

```powershell
.\.venv\Scripts\python.exe app.py
```

Abra http://127.0.0.1:7860. Si utiliza una instancia local ya creada en `./datos/postgresql/`, puede iniciarla previamente con `.\iniciar_postgresql.ps1`; requiere `pg_ctl` en el `PATH`. Cada integrante configura su propio `./.env` y su entorno `./.venv/` según el [README principal](../README.md).
