#!/usr/bin/env python3
"""
Launcher para el Dashboard Macroeconómico de Bolivia
Este script configura el entorno y ejecuta la aplicación automáticamente.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def main():
    print("=" * 50)
    print("    Dashboard Macroeconómico de Bolivia")
    print("=" * 50)
    print()
    
    # Obtener directorio del script
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print(f"📁 Directorio de trabajo: {script_dir}")
    
    # Verificar entorno virtual
    venv_path = script_dir / ".venv"
    if not venv_path.exists():
        print("❌ Error: No se encontró el entorno virtual (.venv)")
        print("   Por favor, ejecute primero el script de instalación")
        input("\nPresione Enter para salir...")
        sys.exit(1)
    
    # Verificar archivo principal
    app_path = script_dir / "src" / "proyectomacro" / "app.py"
    if not app_path.exists():
        print("❌ Error: No se encontró el archivo principal de la aplicación")
        print(f"   Archivo esperado: {app_path}")
        input("\nPresione Enter para salir...")
        sys.exit(1)
    
    print("🔧 Configurando entorno...")
    
    # Configurar variables de entorno
    src_path = str(script_dir / "src")
    current_pythonpath = os.environ.get("PYTHONPATH", "")
    os.environ["PYTHONPATH"] = f"{src_path}:{current_pythonpath}"
    
    # Determinar ejecutable de Python del entorno virtual
    if sys.platform.startswith("win"):
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    if not python_exe.exists():
        print(f"❌ Error: No se encontró el ejecutable de Python: {python_exe}")
        input("\nPresione Enter para salir...")
        sys.exit(1)
    
    print("✅ Entorno configurado correctamente")
    print()
    print("🚀 Iniciando el dashboard...")
    print("   Una vez iniciado, se abrirá automáticamente en su navegador")
    print("   URL: http://127.0.0.1:8050")
    print()
    print("   Para detener el servidor, presione Ctrl+C en esta ventana")
    print()
    
    try:
        # Iniciar la aplicación en un proceso separado
        process = subprocess.Popen(
            [str(python_exe), str(app_path)],
            cwd=str(script_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Esperar un momento para que el servidor inicie
        time.sleep(3)
        
        # Abrir navegador automáticamente
        try:
            webbrowser.open("http://127.0.0.1:8050")
            print("🌐 Navegador abierto automáticamente")
        except Exception as e:
            print(f"⚠️  No se pudo abrir el navegador automáticamente: {e}")
            print("   Abra manualmente: http://127.0.0.1:8050")
        
        print()
        print("📊 Dashboard ejecutándose... Presione Ctrl+C para detener")
        
        # Esperar a que el proceso termine
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo el dashboard...")
        try:
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("✅ Dashboard detenido correctamente")
    
    except Exception as e:
        print(f"\n❌ Error al ejecutar la aplicación: {e}")
    
    print("\n📊 Dashboard cerrado. ¡Gracias por usar el sistema!")
    input("\nPresione Enter para salir...")

if __name__ == "__main__":
    main()
