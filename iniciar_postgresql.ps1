# Inicia la instancia local exclusiva del proyecto; no requiere administrador.
$ErrorActionPreference = 'Stop'
$directorioProyecto = $PSScriptRoot
$directorioDatos = Join-Path $directorioProyecto 'datos\postgresql'
$comandoControl = Get-Command pg_ctl -CommandType Application -ErrorAction SilentlyContinue
if (-not $comandoControl) {
    throw 'No se encuentra pg_ctl. Agrega la carpeta bin de tu instalacion PostgreSQL al PATH.'
}
$ejecutableControl = $comandoControl.Source
if (-not (Test-Path -LiteralPath (Join-Path $directorioDatos 'PG_VERSION'))) {
    throw 'No existe la instancia local configurada.'
}
& $ejecutableControl -D $directorioDatos status
if ($LASTEXITCODE -eq 0) { exit 0 }
$archivoRegistro = Join-Path $directorioProyecto 'datos\postgresql-servidor.log'
$argumentosControl = @('-D', ('"' + $directorioDatos + '"'), '-l', ('"' + $archivoRegistro + '"'), '-w', 'start')
$procesoControl = Start-Process -FilePath $ejecutableControl -ArgumentList $argumentosControl -WindowStyle Hidden -PassThru
$procesoControl.WaitForExit()
if ($procesoControl.ExitCode -ne 0) { throw 'No se pudo iniciar PostgreSQL. Revisa datos\postgresql-servidor.log.' }
