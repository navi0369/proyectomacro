#!/bin/bash
# Script bash para ejecutar la exportación de tablas a Excel
# Uso: ./exportar.sh

echo "🚀 Iniciando exportación de tablas..."
echo ""

# Activar entorno virtual si existe
if [ -f "../.venv/bin/activate" ]; then
    echo "📦 Activando entorno virtual..."
    source ../.venv/bin/activate
fi

# Ejecutar script de Python
python3 exportar_tablas_excel.py

echo ""
echo "✅ Exportación finalizada!"
echo "📂 Los archivos están en: ./tablas_excel/"
