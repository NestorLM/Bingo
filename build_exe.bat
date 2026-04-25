@echo off
setlocal

set "PROJECT_DIR=%~dp0"
set "TMP_BUILD=%TEMP%\bingo_pyinstaller_build"
set "TMP_DIST=%TEMP%\bingo_pyinstaller_dist"
set "OUTPUT_FILE=dist\launcher.exe"

echo ======================================
echo   Bingo - Compilacion de Ejecutable
echo ======================================

echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en PATH.
    goto :end_fail
)

echo [2/4] Instalando dependencias del proyecto...
if exist requiments.txt (
    python -m pip install -r requiments.txt
) else (
    echo ADVERTENCIA: No se encontro requiments.txt, se omite instalacion.
)

echo [3/4] Instalando/actualizando PyInstaller...
python -m pip install --upgrade pyinstaller

echo [4/4] Generando launcher.exe...
if exist "%TMP_BUILD%" rd /s /q "%TMP_BUILD%"
if exist "%TMP_DIST%" rd /s /q "%TMP_DIST%"

python -m PyInstaller --noconfirm --onefile --noconsole --workpath "%TMP_BUILD%" --distpath "%TMP_DIST%" --specpath "%TMP_BUILD%" --hidden-import app --hidden-import Cartela --hidden-import Sorteo --add-data "%PROJECT_DIR%templates;templates" --add-data "%PROJECT_DIR%static;static" "%PROJECT_DIR%launcher.py"
if errorlevel 1 (
    echo ERROR: Fallo la compilacion del ejecutable.
    goto :end_fail
)

if not exist "%PROJECT_DIR%dist" mkdir "%PROJECT_DIR%dist"
copy /Y "%TMP_DIST%\launcher.exe" "%PROJECT_DIR%dist\launcher.exe" >nul
if errorlevel 1 (
    echo ADVERTENCIA: dist\launcher.exe esta en uso. Se creara una copia con fecha/hora.
    for /f "tokens=1-2 delims=:" %%a in ("%time%") do set "HH=%%a" & set "MM=%%b"
    set "HH=%HH: =0%"
    set "STAMP=%date:~6,4%%date:~3,2%%date:~0,2%_%HH%%MM%"
    copy /Y "%TMP_DIST%\launcher.exe" "%PROJECT_DIR%dist\launcher_%STAMP%.exe" >nul
    if errorlevel 1 (
        echo ERROR: No se pudo copiar ningun ejecutable a dist\
        goto :end_fail
    )
    set "OUTPUT_FILE=dist\launcher_%STAMP%.exe"
    echo Ejecutable alternativo generado en: dist\launcher_%STAMP%.exe
)

echo.
echo Compilacion completada con exito.
echo Ejecutable generado en: %OUTPUT_FILE%
goto :end_ok

:end_fail
echo.
echo Proceso finalizado con errores.
exit /b 1

:end_ok
exit /b 0
