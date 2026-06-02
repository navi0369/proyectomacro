#!/usr/bin/env python3
import sqlite3
import pandas as pd
from pathlib import Path
import sys

# Paths
DB_PATH = Path("proyectomacro.db")
OUTPUT_PATH = Path("/home/navi/crecimiento_economico_bolivia_2006_2026.xlsx")

def main():
    print("===========================================================================")
    print("📊 GENERANDO EXCEL ESTRUCTURADO: PIB POR TIPO DE GASTO (2006-2026)")
    print("===========================================================================")
    
    if not DB_PATH.exists():
        print(f"❌ Error: No se encontró la base de datos en {DB_PATH.resolve()}")
        sys.exit(1)
        
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Cargar datos de PIB por Tipo de Gasto
    print("   📖 Cargando datos de PIB Real por Tipo de Gasto (PIB_Real_Gasto)...")
    query_gasto = "SELECT * FROM PIB_Real_Gasto WHERE año >= 2005 ORDER BY año"
    df_gasto = pd.read_sql(query_gasto, conn)
    
    # 2. Agregar proyecciones del FMI para 2025 y 2026 (WEO Abril 2026)
    #    Tasa de crecimiento real del PIB boliviano: 2025 (-1.2%) y 2026 (-3.3%)
    print("   🔮 Aplicando proyecciones del FMI para 2025 y 2026...")
    row_2024 = df_gasto[df_gasto['año'] == 2024].iloc[0]
    
    # Proyección 2025 (-1.2% de crecimiento condicional)
    rate_2025 = -0.012
    row_2025 = {
        'año': 2025,
        'consumo_privado': row_2024['consumo_privado'] * (1 + rate_2025),
        'consumo_publico': row_2024['consumo_publico'] * (1 + rate_2025),
        'gastos_consumo': (row_2024['consumo_privado'] + row_2024['consumo_publico']) * (1 + rate_2025),
        'formacion_capital': row_2024['formacion_capital'] * (1 + rate_2025),
        'exportacion_bienes_servicios': row_2024['exportacion_bienes_servicios'] * (1 + rate_2025),
        'importacion_bienes': row_2024['importacion_bienes'] * (1 + rate_2025),
        'pib_real_base_1990': row_2024['pib_real_base_1990'] * (1 + rate_2025)
    }
    
    # Proyección 2026 (-3.3% de crecimiento condicional)
    rate_2026 = -0.033
    row_2026 = {
        'año': 2026,
        'consumo_privado': row_2025['consumo_privado'] * (1 + rate_2026),
        'consumo_publico': row_2025['consumo_publico'] * (1 + rate_2026),
        'gastos_consumo': (row_2025['consumo_privado'] + row_2025['consumo_publico']) * (1 + rate_2026),
        'formacion_capital': row_2025['formacion_capital'] * (1 + rate_2026),
        'exportacion_bienes_servicios': row_2025['exportacion_bienes_servicios'] * (1 + rate_2026),
        'importacion_bienes': row_2025['importacion_bienes'] * (1 + rate_2026),
        'pib_real_base_1990': row_2025['pib_real_base_1990'] * (1 + rate_2026)
    }
    
    # Concatenar proyecciones
    df_gasto = pd.concat([df_gasto, pd.DataFrame([row_2025, row_2026])], ignore_index=True)
    
    # -------------------------------------------------------------------------
    # HOJA 1: Variaciones Absolutas (Delta PIB_t = PIB_t - PIB_{t-1})
    # -------------------------------------------------------------------------
    print("   🧮 Generando Hoja 1: Variaciones Absolutas (C + I + G + X - M)...")
    df_abs = pd.DataFrame()
    df_abs['Año'] = df_gasto['año']
    df_abs['Consumo Privado (C)'] = df_gasto['consumo_privado'].diff()
    df_abs['Inversión (I)'] = df_gasto['formacion_capital'].diff()
    df_abs['Consumo Público (G)'] = df_gasto['consumo_publico'].diff()
    df_abs['Exportaciones (X)'] = df_gasto['exportacion_bienes_servicios'].diff()
    df_abs['Importaciones (M)'] = df_gasto['importacion_bienes'].diff()
    df_abs['PIB Real Total'] = df_gasto['pib_real_base_1990'].diff()
    
    df_abs_final = df_abs[df_abs['Año'] >= 2006].copy()
    
    # -------------------------------------------------------------------------
    # HOJA 2: Variaciones Porcentuales (pct_change * 100)
    # -------------------------------------------------------------------------
    print("   📈 Generando Hoja 2: Variaciones Porcentuales (Tasas de Crecimiento)...")
    df_pct = pd.DataFrame()
    df_pct['Año'] = df_gasto['año']
    df_pct['Consumo Privado (C) (%)'] = df_gasto['consumo_privado'].pct_change() * 100
    df_pct['Inversión (I) (%)'] = df_gasto['formacion_capital'].pct_change() * 100
    df_pct['Consumo Público (G) (%)'] = df_gasto['consumo_publico'].pct_change() * 100
    df_pct['Exportaciones (X) (%)'] = df_gasto['exportacion_bienes_servicios'].pct_change() * 100
    df_pct['Importaciones (M) (%)'] = df_gasto['importacion_bienes'].pct_change() * 100
    df_pct['PIB Real Total (%)'] = df_gasto['pib_real_base_1990'].pct_change() * 100
    
    df_pct_final = df_pct[df_pct['Año'] >= 2006].copy()
    
    # -------------------------------------------------------------------------
    # HOJA 3: PIB por Tipo de Gasto (Niveles en Miles de Bs constantes de 1990)
    # -------------------------------------------------------------------------
    print("   📊 Generando Hoja 3: PIB por Tipo de Gasto (Niveles)...")
    df_niveles = pd.DataFrame()
    df_niveles['Año'] = df_gasto['año']
    df_niveles['Consumo Privado (C)'] = df_gasto['consumo_privado']
    df_niveles['Inversión (I)'] = df_gasto['formacion_capital']
    df_niveles['Consumo Público (G)'] = df_gasto['consumo_publico']
    df_niveles['Exportaciones (X)'] = df_gasto['exportacion_bienes_servicios']
    df_niveles['Importaciones (M)'] = df_gasto['importacion_bienes']
    df_niveles['PIB Real Total'] = df_gasto['pib_real_base_1990']
    
    df_niveles_final = df_niveles[df_niveles['Año'] >= 2006].copy()
    
    # -------------------------------------------------------------------------
    # 6. Escribir todas las hojas en el archivo Excel
    # -------------------------------------------------------------------------
    print(f"   💾 Escribiendo archivo Excel en {OUTPUT_PATH}...")
    try:
        with pd.ExcelWriter(OUTPUT_PATH, engine='openpyxl') as writer:
            df_abs_final.to_excel(writer, sheet_name="1. Variaciones Absolutas", index=False)
            df_pct_final.to_excel(writer, sheet_name="2. Variaciones Porcentuales", index=False)
            df_niveles_final.to_excel(writer, sheet_name="3. PIB por Tipo de Gasto", index=False)
            
        print("   ✅ Archivo Excel escrito con éxito.")
    except Exception as e:
        print(f"   ❌ Error al escribir el archivo Excel: {e}")
        sys.exit(1)
        
    conn.close()
    
    print("\n" + "=" * 75)
    print("🎉 EXCEL ACTUALIZADO CON ÉXITO!")
    print(f"📂 Archivo generado en: {OUTPUT_PATH.resolve()}")
    print("===========================================================================")

if __name__ == "__main__":
    main()
