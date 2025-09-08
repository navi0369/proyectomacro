#!/usr/bin/env python3
"""
Script de inicio para el Dashboard Macroeconómico de Bolivia
Optimizado para despliegue en Render y desarrollo local
"""
import os
import sys

# Asegurar que el directorio actual esté en Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Agregar src al path para imports directos
src_path = os.path.join(current_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    # Intentar importar desde la estructura instalada
    from proyectomacro.app import app, server
except ImportError as e:
    print(f"Error importando desde proyectomacro: {e}")
    try:
        # Fallback: importar desde src directamente
        sys.path.insert(0, os.path.join(current_dir, 'src'))
        from proyectomacro.app import app, server
    except ImportError as e2:
        print(f"Error en fallback import: {e2}")
        print("Estructura de directorios:")
        for root, dirs, files in os.walk(current_dir):
            level = root.replace(current_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                if file.endswith('.py'):
                    print(f"{subindent}{file}")
        sys.exit(1)

def main():
    """Función principal para ejecutar el dashboard"""
    # Configuración para producción/desarrollo
    debug_mode = os.environ.get('DASH_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('DASH_HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8050))
    
    print(f"Iniciando Dashboard Macroeconómico de Bolivia...")
    print(f"Debug: {debug_mode}")
    print(f"Host: {host}")
    print(f"Puerto: {port}")
    
    app.run(
        debug=debug_mode,
        host=host,
        port=port,
        dev_tools_hot_reload=debug_mode,
        dev_tools_ui=debug_mode,
    )

if __name__ == "__main__":
    main()
