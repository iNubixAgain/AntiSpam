# Detector académico: consulta de datasets en PostgreSQL

Proyecto 5 · Fundamentos de Inteligencia Artificial · Universidad Tecnológica de Querétaro.

La aplicación trabaja únicamente con registros existentes. Busca coincidencias exactas normalizadas por canal y muestra la etiqueta original con su procedencia. Los mensajes no encontrados, los registros sin etiqueta y las etiquetas contradictorias quedan sin clasificación. No hay entrenamiento, predicciones por reglas ni inserción de datos.

## Ejecutar el proyecto

Todas las rutas de archivos y comandos de esta guía son relativas a la raíz del proyecto: la carpeta que contiene `app.py` y `requirements.txt`, independientemente de su nombre o ubicación. Abra esa carpeta en VS Code y utilice su terminal integrada.

Si ya tiene configurada la instancia local en `./datos/postgresql/`, iníciela y abra la aplicación:

```powershell
.\iniciar_postgresql.ps1
.\.venv\Scripts\python.exe app.py
```

Si PostgreSQL ya funciona como servicio o usa otra instancia, ejecute únicamente el segundo comando con la conexión correspondiente en `./.env`. El iniciador requiere `pg_ctl` disponible en el `PATH` y no crea una instancia nueva.

Abra http://127.0.0.1:7860. Gradio funciona localmente sin enlace público. Seleccione SMS, Correo o Chat antes de consultar. Limpiar restablece únicamente los campos de la interfaz. El explorador permite filtros y búsqueda paginada, con ejemplos limitados y ocultación parcial de datos personales. Enron oculta siempre el contenido.

Este es el único README del proyecto y está en la raíz. La documentación técnica y los dumps se encuentran en `./Documentacion/`; la portada complementaria está en [PORTADA.md](.github/PORTADA.md). Los enlaces entre documentos son relativos al archivo que está leyendo.

## Configuración

Se requiere Python 3.10 o superior, PostgreSQL 17 y las dependencias:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

En VS Code seleccione `.venv` como intérprete. No necesita activar el entorno para usar los comandos anteriores.

La instalación original utiliza `127.0.0.1:5433`, con archivos persistentes en `./datos/postgresql/`. Cada integrante debe configurar en `./.env` el host, puerto y credenciales de su propia instalación; no es obligatorio usar ese puerto. La cuenta de consulta debe tener únicamente SELECT sobre fuentes y mensajes. En la instalación original se llama `antispam_lectura` y el rol anterior `antispam` tiene NOLOGIN. La conexión de Python también establece transacciones de solo lectura.

En la instalación original, `./.env.postgres-local` guarda la credencial administrativa de mantenimiento; la aplicación no la carga y los compañeros no necesitan copiarla. El administrador de PostgreSQL conserva sus facultades de mantenimiento: el bloqueo de escritura se aplica a la cuenta de la aplicación. No publique credenciales ni el contenido de `./datos/`.

Para otra instalación, copie `./.env.example` a `./.env` si todavía no existe y configure una cuenta de solo lectura para una base con el esquema y datos ya presentes:

```powershell
# Ejecutar solo si todavía no existe .env.
Copy-Item .\.env.example .\.env
```

No sobrescriba una configuración existente. Cada integrante debe crear su propio entorno `./.venv/`; no se comparte esa carpeta. Un clon de Git no incluye `./.env`, `./datos/` ni los dumps. El equipo debe transferir el respaldo por un canal privado y restaurarlo en la instalación de cada integrante mediante una cuenta administrativa. Esta versión de la aplicación no crea ni importa bases y conserva su acceso de solo lectura.

## Datos conservados

| Fuente | Total | ham | spam |
| --- | ---: | ---: | ---: |
| UCI SMS Spam Collection | 5,574 | 4,827 | 747 |
| Apache SpamAssassin | 6,024 | 4,150 | 1,874 |

Total conservado: 11,598 registros reales. SpamAssassin rechazó 22 registros durante la importación original. Enron no fue importado y no se inventaron registros para completarlo. Las descargas comprimidas ya importadas se retiraron durante la limpieza; los datos PostgreSQL y el respaldo inicial se conservan.

## Comprobar el funcionamiento

Abra la aplicación, entre en Explorar datasets y pulse Buscar / actualizar estado. Debe indicar conexión en modo de solo lectura y mostrar los totales anteriores. Un mensaje nuevo debe aparecer sin clasificación; Limpiar debe vaciar los campos.

GitHub muestra este README como entrada principal del proyecto. El proyecto no requiere herramientas de desarrollo adicionales para ejecutarse.

## Respaldo

`Documentacion/antispam-completo.dump` es el respaldo completo de la base actual, generado con pg_dump (esquema, datos y secuencias, sin filtros de tablas). `Documentacion/respaldo-inicial.dump` conserva el respaldo anterior. Los dumps contienen datos reales y están excluidos de Git. Las credenciales y los roles globales del servidor no se incluyen en estos respaldos de base de datos.

Para crear otro respaldo sin sobrescribir los existentes:

```powershell
.\.venv\Scripts\python.exe .\tools\exportar_dump.py .\Documentacion\respaldo-consulta.dump
```

El comando requiere `pg_dump` disponible en el `PATH`. Configure el `PATH` con la carpeta `bin` de la instalación de PostgreSQL de cada equipo; no hay una ubicación de instalación única para todos los integrantes.

La restauración es una tarea administrativa externa a esta aplicación. Debe realizarse con pg_restore en una base nueva, nunca contra la base activa sin autorización. El usuario de lectura no puede restaurar ni insertar datos. No cambie el respaldo ni las credenciales de otro integrante.

Las instrucciones de restauración, exportación y comprobación están junto a los scripts en [tools/GUIA_TOOLS.md](tools/GUIA_TOOLS.md). La aplicación no importa estas utilidades ni utiliza su conexión administrativa.

## Problemas frecuentes

- Error de conexión: ejecute `iniciar_postgresql.ps1` y revise DATABASE_URL sin compartir la contraseña.
- Sin clasificación: no hubo coincidencia exacta para el canal, faltaba etiqueta o había etiquetas contradictorias.
- Base vacía: esta versión no descarga ni importa registros.
- Puerto 7860 ocupado: cierre la otra instancia de Gradio antes de iniciar.
- No elimine su entorno `./.venv/`, su configuración `./.env` ni, si utiliza la instancia del proyecto, `./datos/postgresql/` y `./iniciar_postgresql.ps1`.

Consulte [DOCUMENTACION.md](Documentacion/DOCUMENTACION.md) para arquitectura, fuentes y privacidad.
