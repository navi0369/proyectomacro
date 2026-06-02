#!/bin/bash
# Script para ejecutar la exportación estructurada de variables a Excel
# Uso: ./exportar_variables.sh

echo "🚀 Iniciando exportación estructurada de variables..."
echo ""

# Activar el entorno virtual del proyecto
if [ -d "../venv" ]; then
    echo "📦 Activando entorno virtual del proyecto (venv)..."
    source ../venv/bin/activate
elif [ -d "../.venv" ]; then
    echo "📦 Activando entorno virtual del proyecto (.venv)..."
    source ../.venv/bin/activate
else
    echo "⚠️  No se encontró la carpeta 'venv' o '.venv' en el directorio padre."
fi

# Ejecutar el script de exportación con Python
python3 exportar_variables.py

echo ""
echo "✅ Proceso completado!"
echo "📂 Las carpetas por variable y sus archivos Excel están en: ./excels/"
