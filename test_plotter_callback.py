#!/usr/bin/env python3
"""
Script de prueba para verificar el callback update_columns_options
"""
import sys
sys.path.append('src')

# Simular el comportamiento del callback
from func_auxiliares.graficos_utils import get_df
from func_auxiliares.config import DB_PATH
import sqlite3

def get_available_tables():
    """Obtiene lista de tablas disponibles en la base de datos"""
    try:
        with sqlite3.connect(str(DB_PATH)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            return sorted(tables)
    except Exception as e:
        print(f"Error obteniendo tablas: {e}")
        return []

def get_table_columns(table_name):
    """Obtener columnas de una tabla específica"""
    try:
        query = f"PRAGMA table_info({table_name})"
        columns_df = get_df(query, conn_str=str(DB_PATH))
        return columns_df['name'].tolist()
    except Exception as e:
        print(f"Error obteniendo columnas de {table_name}: {e}")
        return []

def simulate_update_columns_options(selected_table):
    """Simular el callback update_columns_options"""
    if not selected_table:
        return [], []
    
    try:
        # Usar get_table_columns igual que en calculadora.py
        columns = get_table_columns(selected_table)
        # Filtrar columnas numéricas típicas (excluir año que suele ser índice)
        numeric_columns = [col for col in columns if col.lower() not in ['año', 'year', 'fecha', 'date']]
        
        options = [{"label": col, "value": col} for col in numeric_columns]
        return options, []
    except Exception as e:
        print(f"Error obteniendo columnas: {e}")
        return [], []

# Test del flujo completo
if __name__ == "__main__":
    print("🧪 Test del callback update_columns_options")
    print("=" * 50)
    
    # 1. Obtener tablas disponibles
    tables = get_available_tables()
    print(f"📊 Tablas disponibles: {len(tables)}")
    
    # 2. Probar con varias tablas
    test_tables = tables[:3] if len(tables) >= 3 else tables
    
    for i, table in enumerate(test_tables, 1):
        print(f"\n{i}. Probando tabla: '{table}'")
        options, value = simulate_update_columns_options(table)
        
        print(f"   ✅ Opciones generadas: {len(options)}")
        print(f"   📋 Columnas disponibles: {[opt['label'] for opt in options]}")
        print(f"   🎯 Valor inicial: {value}")
    
    # 3. Probar caso edge: tabla inexistente
    print(f"\n4. Probando tabla inexistente")
    options, value = simulate_update_columns_options("tabla_inexistente")
    print(f"   ✅ Opciones para tabla inexistente: {len(options)}")
    print(f"   🎯 Valor para tabla inexistente: {value}")
    
    # 4. Probar caso edge: None
    print(f"\n5. Probando con None")
    options, value = simulate_update_columns_options(None)
    print(f"   ✅ Opciones para None: {len(options)}")
    print(f"   🎯 Valor para None: {value}")
    
    print("\n" + "=" * 50)
    print("✅ Test completado exitosamente")
