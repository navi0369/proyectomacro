#!/bin/bash

# Script para ejecutar el Dashboard Macroeconómico de Bolivia
# Autor: Dashboard Macro Team
# Fecha: $(date +%Y-%m-%d)

echo "=========================================="
echo "  Dashboard Macroeconómico de Bolivia"
echo "=========================================="
echo ""

# Obtener el directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 Directorio de trabajo: $SCRIPT_DIR"

# Verificar si existe el entorno virtual
if [ ! -d ".venv" ]; then
    echo "❌ Error: No se encontró el entorno virtual (.venv)"
    echo "   Por favor, ejecute primero el script de instalación"
    echo ""
    read -p "Presione Enter para salir..."
    exit 1
fi

# Verificar si existe el archivo principal
if [ ! -f "src/proyectomacro/app.py" ]; then
    echo "❌ Error: No se encontró el archivo principal de la aplicación"
    echo "   Archivo esperado: src/proyectomacro/app.py"
    echo ""
    read -p "Presione Enter para salir..."
    exit 1
fi

# Activar entorno virtual y configurar variables
echo "🔧 Configurando entorno..."
source .venv/bin/activate

# Agregar src al PYTHONPATH para imports
export PYTHONPATH="$SCRIPT_DIR/src:$PYTHONPATH"

echo "✅ Entorno configurado correctamente"
echo ""
echo "🚀 Iniciando el dashboard..."
echo "   Una vez iniciado, abra su navegador en: http://127.0.0.1:8050"
echo ""
echo "   Para detener el servidor, presione Ctrl+C"
echo ""

# Ejecutar la aplicación
python src/proyectomacro/app.py

echo ""
echo "📊 Dashboard cerrado. ¡Gracias por usar el sistema!"
echo ""
read -p "Presione Enter para salir..."
