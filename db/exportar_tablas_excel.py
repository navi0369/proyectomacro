#!/usr/bin/env python3
"""
Script para exportar todas las tablas de la base de datos SQLite a archivos Excel.
Organiza las exportaciones por sección según la configuración en pages.yml.

Uso:
    python exportar_tablas_excel.py

Autor: Generado automáticamente
Fecha: 2025-10-16
"""

import sqlite3
import pandas as pd
import yaml
from pathlib import Path
import sys
import os

# ══════════════════════════════════════════════════════════════════════
# 1. CONFIGURACIÓN
# ══════════════════════════════════════════════════════════════════════

# Rutas relativas desde db/
DB_PATH = Path("proyectomacro.db")
PAGES_YML_PATH = Path("../src/proyectomacro/config/pages.yml")
OUTPUT_BASE_DIR = Path("tablas_excel")

# ══════════════════════════════════════════════════════════════════════
# 2. FUNCIONES AUXILIARES
# ══════════════════════════════════════════════════════════════════════

def cargar_configuracion_secciones(yml_path: Path) -> dict:
    """
    Lee pages.yml y construye un diccionario {nombre_tabla: seccion}.
    
    Returns:
        dict: Mapeo de tabla -> sección
    """
    if not yml_path.exists():
        print(f"⚠️  Advertencia: No se encontró {yml_path}")
        return {}
    
    with open(yml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    tabla_a_seccion = {}
    
    for seccion_key, seccion_data in config.get('secciones', {}).items():
        seccion_name = seccion_data.get('name', seccion_key)
        # Normalizar nombre de sección para carpeta (sin espacios, guiones bajos)
        seccion_folder = seccion_key  # usa la clave como nombre de carpeta
        
        for tabla_key, tabla_info in seccion_data.get('tablas', {}).items():
            tabla_nombre = tabla_info.get('tabla')
            if tabla_nombre:
                tabla_a_seccion[tabla_nombre] = {
                    'seccion': seccion_folder,
                    'seccion_name': seccion_name,
                    'label': tabla_info.get('label', tabla_nombre)
                }
    
    return tabla_a_seccion


def obtener_tablas_db(db_path: Path) -> list:
    """
    Lista todas las tablas en la base de datos SQLite.
    
    Returns:
        list: Lista de nombres de tablas
    """
    if not db_path.exists():
        print(f"❌ Error: Base de datos no encontrada en {db_path}")
        sys.exit(1)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)
    
    tablas = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return tablas


def exportar_tabla_a_excel(tabla: str, db_path: Path, output_path: Path) -> bool:
    """
    Exporta una tabla de SQLite a un archivo Excel.
    
    Args:
        tabla: Nombre de la tabla
        db_path: Ruta a la base de datos
        output_path: Ruta del archivo Excel de salida
    
    Returns:
        bool: True si la exportación fue exitosa
    """
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql(f"SELECT * FROM {tabla}", conn)
        conn.close()
        
        # Crear directorio si no existe
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Exportar a Excel
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        return True
    
    except Exception as e:
        print(f"   ❌ Error al exportar {tabla}: {e}")
        return False


# ══════════════════════════════════════════════════════════════════════
# 3. FUNCIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════════════════

def main():
    """
    Función principal que coordina la exportación de todas las tablas.
    """
    print("=" * 70)
    print("🔄 EXPORTACIÓN DE TABLAS A EXCEL")
    print("=" * 70)
    print()
    
    # 1. Cargar configuración de secciones
    print("📋 Cargando configuración de secciones...")
    tabla_a_seccion = cargar_configuracion_secciones(PAGES_YML_PATH)
    print(f"   ✓ Configuración cargada: {len(tabla_a_seccion)} tablas mapeadas")
    print()
    
    # 2. Obtener lista de tablas de la base de datos
    print("🗄️  Consultando tablas en la base de datos...")
    tablas = obtener_tablas_db(DB_PATH)
    print(f"   ✓ Encontradas {len(tablas)} tablas en la base de datos")
    print()
    
    # 3. Exportar cada tabla
    print("📤 Iniciando exportación de tablas...")
    print("-" * 70)
    
    exitosas = 0
    fallidas = 0
    sin_seccion = 0
    
    for tabla in tablas:
        # Determinar sección de destino
        if tabla in tabla_a_seccion:
            info = tabla_a_seccion[tabla]
            seccion_folder = info['seccion']
            label = info['label']
            output_dir = OUTPUT_BASE_DIR / seccion_folder
        else:
            # Tablas sin sección van a una carpeta "sin_clasificar"
            output_dir = OUTPUT_BASE_DIR / "sin_clasificar"
            label = tabla
            sin_seccion += 1
        
        output_path = output_dir / f"{tabla}.xlsx"
        
        print(f"📊 {tabla}")
        print(f"   → Destino: {output_path}")
        
        # Exportar
        if exportar_tabla_a_excel(tabla, DB_PATH, output_path):
            print(f"   ✅ Exportada exitosamente")
            exitosas += 1
        else:
            fallidas += 1
        
        print()
    
    # 4. Resumen
    print("=" * 70)
    print("📊 RESUMEN DE EXPORTACIÓN")
    print("=" * 70)
    print(f"✅ Exitosas:        {exitosas}")
    print(f"❌ Fallidas:        {fallidas}")
    print(f"⚠️  Sin clasificar: {sin_seccion}")
    print(f"📁 Total:           {len(tablas)}")
    print()
    print(f"📂 Directorio de salida: {OUTPUT_BASE_DIR.resolve()}")
    print("=" * 70)
    
    # Listar estructura de carpetas creadas
    if OUTPUT_BASE_DIR.exists():
        print()
        print("📁 Estructura de carpetas creadas:")
        print("-" * 70)
        for seccion_dir in sorted(OUTPUT_BASE_DIR.iterdir()):
            if seccion_dir.is_dir():
                num_archivos = len(list(seccion_dir.glob("*.xlsx")))
                print(f"   📂 {seccion_dir.name}/ ({num_archivos} archivos)")
        print("=" * 70)


# ══════════════════════════════════════════════════════════════════════
# 4. PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Exportación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
