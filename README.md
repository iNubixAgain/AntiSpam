# Detector de spam y mensajes fraudulentos

**Proyecto 5 — Fundamentos de Inteligencia Artificial**  
Universidad Tecnológica de Querétaro

## Descripción

Prototipo académico desarrollado con **Python y Gradio** para demostrar cómo un usuario podría revisar mensajes recibidos por SMS, correo electrónico o chat.

La aplicación permite ingresar un mensaje, elegir su canal y visualizar cuatro resultados:

- **Clasificación:** normal, spam o potencialmente fraudulento.
- **Nivel de riesgo:** bajo, medio o alto.
- **Indicadores:** palabras o señales encontradas en el texto.
- **Recomendación:** consejo general de precaución en lenguaje sencillo.

> **Importante:** esta primera versión **no utiliza un modelo de inteligencia artificial entrenado**. Los resultados se obtienen mediante reglas temporales basadas en coincidencias de texto. No deben utilizarse para decidir si un mensaje real es seguro.

## Requisitos

- Windows 10/11, macOS o Linux.
- **Python 3.10 o superior**, con `pip` y `venv` disponibles.
- Un editor de código (recomendado: Visual Studio Code).
- Conexión a Internet para instalar Gradio por primera vez.

## Estructura inicial

```text
DetectorSpam/
├── app.py             # Interfaz y funciones del prototipo
├── README.md          # Instrucciones de instalación y ejecución
├── DOCUMENTACION.md   # Explicación técnica y del funcionamiento
└── .venv/             # Entorno virtual local (no subir al repositorio)
```

> Este README supone que `app.py` contiene el código del prototipo desarrollado en clase. No es necesario crear otros archivos Python para esta primera versión.

## Instalación en Windows (PowerShell y VS Code)

### 1. Abrir el proyecto

Abre la carpeta `DetectorSpam` en Visual Studio Code y selecciona **Terminal > Nueva terminal**. Comprueba que la terminal se encuentre dentro de la carpeta del proyecto.

### 2. Comprobar Python

```powershell
py --version
```

Debe mostrar una versión 3.10 o superior.

### 3. Crear el entorno virtual (solo la primera vez)

```powershell
py -m venv .venv
```

Esto crea un entorno aislado para las dependencias del proyecto. Si `.venv` ya existe y funciona, omite este paso.

### 4. Activar el entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

La terminal normalmente mostrará el prefijo `(.venv)`.

**Si PowerShell bloquea la activación**, no es obligatorio cambiar la política de ejecución. Puedes instalar y ejecutar usando directamente el Python del entorno:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade gradio
.\.venv\Scripts\python.exe app.py
```

### 5. Instalar Gradio

Con el entorno virtual activado:

```powershell
python -m pip install --upgrade gradio
```

Si en el futuro el proyecto incluye un `requirements.txt`, también podrás instalar sus dependencias mediante `python -m pip install -r requirements.txt`.

### 6. Verificar la instalación

```powershell
python -m pip show gradio
```

El comando debe mostrar el nombre del paquete, su versión y su ruta de instalación dentro de `.venv`.

### 7. Ejecutar la aplicación

```powershell
python app.py
```

Abre la dirección que aparezca en la terminal. Con la configuración actual del prototipo, normalmente será:

**http://127.0.0.1:7860**

La ventana de terminal debe permanecer abierta mientras se utiliza la aplicación.

### 8. Detener la aplicación

Presiona **Ctrl + C** en la terminal. Para desactivar el entorno virtual, ejecuta:

```powershell
deactivate
```

## Ejecución posterior

Cuando regreses al proyecto otro día, **no necesitas recrear el entorno ni reinstalar Gradio**. Solo abre la carpeta y ejecuta:

```powershell
.\.venv\Scripts\Activate.ps1
python app.py
```

## Instrucciones rápidas para macOS o Linux

Desde una terminal abierta en la carpeta del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade gradio
python app.py
```

## Pruebas de demostración

Utiliza mensajes **inventados**, sin datos personales:

| Mensaje de prueba | Clasificación provisional esperada |
| --- | --- |
| `Hola, nos vemos mañana a las cinco.` | Normal |
| `Tenemos una oferta especial con descuento.` | Spam |
| `Verifica tu cuenta o será bloqueada.` | Potencialmente fraudulento |
| Mensaje vacío | Sin analizar |

También comprueba el botón **Limpiar**: debe vaciar los campos de texto y resultados y devolver el canal a **SMS**.

> Los resultados anteriores solo comprueban que las reglas programadas funcionan como se espera; **no validan la seguridad real de un mensaje**.

## Problemas frecuentes

| Problema | Posible solución |
| --- | --- |
| `py` no se reconoce | Verifica la instalación de Python y el lanzador de Python en Windows. |
| `No module named gradio` | Asegúrate de activar `.venv` e instalar Gradio usando `python -m pip install --upgrade gradio`. |
| PowerShell no permite activar `.venv` | Usa `.\.venv\Scripts\python.exe` directamente, como se indica en el paso 4. |
| No se abre la página | Revisa la URL que muestra la terminal y comprueba que el programa siga en ejecución. |
| El puerto 7860 está ocupado | Cierra otra instancia de Gradio que utilice el puerto o cambia el puerto de lanzamiento en `app.py`. |
| Se modificó `app.py` y no se ven cambios | Detén el programa con Ctrl + C y ejecútalo nuevamente. |

## Privacidad y alcance

- El código inicial **no contiene instrucciones para guardar mensajes en archivos o bases de datos**.
- La interfaz está configurada para escuchar en `127.0.0.1` y usar `share=False`, es decir, **sin crear un enlace público de Gradio**.
- No se debe afirmar que esto impide toda retención temporal o registro del sistema: para las demostraciones, utiliza mensajes ficticios y evita información sensible.
- El clasificador real con aprendizaje automático es una mejora prevista para etapas posteriores.

## Documentación adicional

Consulta [DOCUMENTACION.md](DOCUMENTACION.md) para conocer qué es Gradio, cómo se conectan las funciones con la interfaz y cómo opera el análisis simulado.

**Documentación oficial:** https://www.gradio.app/guides/quickstart
