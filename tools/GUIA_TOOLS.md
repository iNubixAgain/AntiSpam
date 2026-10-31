# Herramientas de AntiSpam

Estas utilidades funcionan aparte de Gradio y usan las mismas dependencias de `requirements.txt`. No requieren herramientas de desarrollo adicionales.

Todos los comandos se ejecutan desde la **raíz del proyecto**, donde está `app.py`. Los archivos recibidos como argumentos se resuelven desde esa raíz y la configuración se carga de `./.env`.

| Archivo | Función |
| --- | --- |
| `exportar_dump.py` | Crear un respaldo completo con pg_dump |
| `importar_bd.py` | Restaurar un dump en una base nueva y vacía |
| `probar_app.py` | Comprobar conexión, permisos, consultas y botones |
| `utilidades.py` | Configuración compartida; no se ejecuta directamente |

## Comprobar la aplicación

Con PostgreSQL iniciado y DATABASE_URL configurada para una cuenta de solo lectura:

```powershell
.\.venv\Scripts\python.exe .\tools\probar_app.py
```

Comprueba permisos, estadísticas, una etiqueta existente si hay datos, entrada vacía y botones Analizar y Limpiar. También verifica que la interfaz no tenga un explorador de datasets. No inserta datos ni imprime contenidos privados. Una base vacía se informa como tal y se omite la comprobación de un registro existente.

Para comprobar también HTTP, abra primero la aplicación en otra terminal y ejecute:

```powershell
.\.venv\Scripts\python.exe .\app.py
```

```powershell
.\.venv\Scripts\python.exe .\tools\probar_app.py --http
```

## Exportar la base

Agregue la carpeta `bin` de su instalación de PostgreSQL al PATH; no hay una ubicación fija para todos los equipos.

```powershell
.\.venv\Scripts\python.exe .\tools\exportar_dump.py .\Documentacion\respaldo-equipo.dump
```

Usa DATABASE_URL y pg_dump oficial. Exporta esquema, datos y secuencias en formato custom, sin contraseñas ni roles globales. No sobrescribe archivos y el directorio destino debe existir. Las credenciales de conexión no se pasan como argumentos de línea de comandos. El repositorio incluye expresamente `Documentacion/antispam-completo.dump` y `Documentacion/ejemplos-antispam-completo.txt`; los respaldos adicionales permanecen excluidos de Git.

## Importar un respaldo en otro equipo

Es una restauración administrativa del dump, **no una importación de nuevos datasets**. La aplicación conserva su cuenta de solo lectura.

1. Cree una base nueva y vacía con una cuenta administrativa. Ejemplo:

   ```powershell
   createdb -h localhost -p 5432 -U postgres antispam_equipo
   ```

2. Coloque el respaldo de confianza en `./Documentacion/`. Configure RESTORE_DATABASE_URL en su propio `./.env` con las credenciales administrativas y esa base nueva como destino. Hay una línea de ejemplo comentada en `./.env.example`. Ajuste host y puerto; codifique caracteres reservados de la contraseña en la URL. No comparta credenciales ni utilice la URL de una base activa.

3. Ejecute:

   ```powershell
   .\.venv\Scripts\python.exe .\tools\importar_bd.py .\Documentacion\antispam-completo.dump
   ```

   Sin argumento utiliza ese mismo dump. Requiere pg_restore en PATH. Rechaza bases de mantenimiento o bases que ya contienen tablas, vistas, secuencias o funciones. No usa --clean. La restauración se hace en una sola transacción, se revierte si pg_restore falla y se verifican los totales al terminar. No use el destino para otras operaciones mientras restaura.

4. La restauración no crea usuarios ni copia permisos de la instalación original. Entre a la base restaurada con su administrador:

   ```powershell
   psql -h localhost -p 5432 -U postgres -d antispam_equipo
   ```

   Si el usuario lector todavía no existe, créelo y asigne su contraseña mediante el diálogo de psql:

   ```sql
   CREATE ROLE antispam_lectura LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;
   \password antispam_lectura
   ```

   Configure una cuenta sin otros privilegios ni pertenencias administrativas:

   ```sql
   REVOKE CREATE ON SCHEMA public FROM PUBLIC;
   REVOKE TEMPORARY ON DATABASE antispam_equipo FROM PUBLIC;
   GRANT CONNECT ON DATABASE antispam_equipo TO antispam_lectura;
   GRANT USAGE ON SCHEMA public TO antispam_lectura;
   GRANT SELECT ON fuentes, mensajes TO antispam_lectura;
   GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO antispam_lectura;
   ALTER ROLE antispam_lectura SET default_transaction_read_only = on;
   ```

5. Ajuste DATABASE_URL en `./.env` para usar el lector y la base `antispam_equipo`. Retire RESTORE_DATABASE_URL cuando termine y ejecute `probar_app.py` antes de abrir Gradio.

Los nombres y el puerto son ejemplos: adáptelos de forma coherente a su instalación. No use una cuenta administrativa como cuenta de la aplicación.

## Ayuda y errores

Cada script admite `--help`. Puede elegir los ejecutables oficiales mediante `--pg-dump` o `--pg-restore`. Si faltan, revise PATH. Si el destino de restauración ya contiene objetos, cree otra base; no borre la base del proyecto. Los errores devuelven código 1 sin mostrar mensajes privados ni contraseñas.

Consulte [la guía de instalación](../Documentacion/GUIA_INSTALACION.md) para instalar y abrir la aplicación, o vuelva a la [portada del proyecto](../README.md).
