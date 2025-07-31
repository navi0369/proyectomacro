#!/bin/bash

# Script de instalación para el Dashboard Macroeconómico de Bolivia
# Este script configura automáticamente el entorno necesario

echo "=========================================="
echo "  Instalador - Dashboard Macroeconómico"
echo "=========================================="
echo ""

# Obtener el directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 Directorio de instalación: $SCRIPT_DIR"

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo "   Por favor, instale Python 3.8 o superior"
    echo ""
    read -p "Presione Enter para salir..."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python encontrado: $(python3 --version)"

# Verificar si ya existe un entorno virtual
if [ -d ".venv" ]; then
    echo "⚠️  Ya existe un entorno virtual. ¿Desea recrearlo? (s/N)"
    read -r recreate
    if [[ $recreate =~ ^[Ss]$ ]]; then
        echo "🗑️  Eliminando entorno virtual existente..."
        rm -rf .venv
    else
        echo "✅ Usando entorno virtual existente"
    fi
fi

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "🔧 Creando entorno virtual..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ Error al crear el entorno virtual"
        echo "   Verifique que python3-venv esté instalado"
        echo "   En Ubuntu/Debian: sudo apt install python3-venv"
        echo ""
        read -p "Presione Enter para salir..."
        exit 1
    fi
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source .venv/bin/activate

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# Verificar si existe requirements.txt
if [ -f "requirements.txt" ]; then
    echo "📦 Instalando dependencias desde requirements.txt..."
    pip install -r requirements.txt
else
    echo "📦 Instalando dependencias básicas..."
    pip install dash dash-bootstrap-components pandas numpy matplotlib sqlite3 plotly
fi

# Hacer ejecutables los scripts de lanzamiento
echo "🔧 Configurando permisos de ejecución..."
chmod +x run_dashboard.sh
chmod +x launch_dashboard.py

echo ""
echo "✅ ¡Instalación completada exitosamente!"
echo ""
echo "Para ejecutar el dashboard, puede usar cualquiera de estos métodos:"
echo "  1. Doble clic en: run_dashboard.sh (Linux/Mac)"
echo "  2. Doble clic en: run_dashboard.bat (Windows)" 
echo "  3. Doble clic en: launch_dashboard.py (Multiplataforma)"
echo "  4. Desde terminal: ./run_dashboard.sh"
echo ""
echo "🌐 El dashboard se abrirá en: http://127.0.0.1:8050"
echo ""
read -p "Presione Enter para salir..."
