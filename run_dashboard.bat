@echo off
title Dashboard Macroeconomico de Bolivia
color 0A

echo ==========================================
echo   Dashboard Macroeconomico de Bolivia
echo ==========================================
echo.

REM Obtener el directorio del script
cd /d "%~dp0"
set SCRIPT_DIR=%CD%

echo 📁 Directorio de trabajo: %SCRIPT_DIR%

REM Verificar si existe el entorno virtual
if not exist ".venv" (
    echo ❌ Error: No se encontro el entorno virtual ^(.venv^)
    echo    Por favor, ejecute primero el script de instalacion
    echo.
    pause
    exit /b 1
)

REM Verificar si existe el archivo principal
if not exist "src\proyectomacro\app.py" (
    echo ❌ Error: No se encontro el archivo principal de la aplicacion
    echo    Archivo esperado: src\proyectomacro\app.py
    echo.
    pause
    exit /b 1
)

REM Activar entorno virtual
echo 🔧 Configurando entorno...
call .venv\Scripts\activate.bat

REM Configurar PYTHONPATH
set PYTHONPATH=%SCRIPT_DIR%\src;%PYTHONPATH%

echo ✅ Entorno configurado correctamente
echo.
echo 🚀 Iniciando el dashboard...
echo    Una vez iniciado, abra su navegador en: http://127.0.0.1:8050
echo.
echo    Para detener el servidor, presione Ctrl+C
echo.

REM Ejecutar la aplicación
python src\proyectomacro\app.py

echo.
echo 📊 Dashboard cerrado. ¡Gracias por usar el sistema!
echo.
pause
