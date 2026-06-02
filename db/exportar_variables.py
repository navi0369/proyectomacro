#!/usr/bin/env python3
import sqlite3
import pandas as pd
from pathlib import Path
import sys
import os

# Configuration paths
DB_PATH = Path("proyectomacro.db")
OUTPUT_BASE_DIR = Path("excels")

# Variables configuration based on the PDF analysis of the 11 econometric variables
VARIABLES_CONFIG = {
    "V1_Exportaciones": {
        "label": "Exportaciones de Bienes y Servicios (V1)",
        "excel_name": "V1_Exportaciones_Bienes_Servicios.xlsx",
        "tables": {
            "balanza_comercial": "SELECT año, exportaciones FROM balanza_comercial"
        }
    },
    "V2_Ingresos_Fiscales": {
        "label": "Ingresos Fiscales (V2)",
        "excel_name": "V2_Ingresos_Fiscales.xlsx",
        "tables": {
            "finanzas_publicas": "SELECT * FROM finanzas_publicas",
            "consolidado_spnf": "SELECT * FROM consolidado_spnf"
        }
    },
    "V3_Resultado_Fiscal": {
        "label": "Balance y Resultado Fiscal (V3)",
        "excel_name": "V3_Resultado_Fiscal.xlsx",
        "tables": {
            "finanzas_publicas": "SELECT * FROM finanzas_publicas",
            "consolidado_spnf": "SELECT * FROM consolidado_spnf"
        }
    },
    "V4_Deuda_Publica": {
        "label": "Deuda Pública Total (V4)",
        "excel_name": "V4_Deuda_Publica_Total.xlsx",
        "tables": {
            "deuda_externa_total": "SELECT * FROM deuda_externa_total",
            "deuda_interna": "SELECT * FROM deuda_interna"
        }
    },
    "V5_Entrada_Divisas": {
        "label": "Entrada de Divisas (V5)",
        "excel_name": "V5_Entrada_Divisas.xlsx",
        "tables": {
            "venta_de_divisas_al_banco_central": "SELECT * FROM venta_de_divisas_al_banco_central",
            "flujo_divisas": "SELECT * FROM flujo_divisas"
        }
    },
    "V6_Reservas_Internacionales": {
        "label": "Reservas Internacionales Netas (V6)",
        "excel_name": "V6_Reservas_Internacionales_Netas.xlsx",
        "tables": {
            "Reservas_oro_divisas": "SELECT año, reservas_totales FROM Reservas_oro_divisas"
        }
    },
    "V7_Tipo_de_Cambio": {
        "label": "Tipo de Cambio Nominal y Real (V7)",
        "excel_name": "V7_Tipo_de_Cambio.xlsx",
        "tables": {
            "cotizacion_oficial_dolar": "SELECT * FROM cotizacion_oficial_dolar"
        }
    },
    "V8_Importaciones": {
        "label": "Importaciones de Bienes y Servicios (V8)",
        "excel_name": "V8_Importaciones.xlsx",
        "tables": {
            "balanza_comercial": "SELECT año, importaciones FROM balanza_comercial"
        }
    },
    "V9_Saldo_Balanza_Comercial": {
        "label": "Saldo de la Balanza Comercial (V9)",
        "excel_name": "V9_Saldo_Balanza_Comercial.xlsx",
        "tables": {
            "balanza_comercial_calculado": "SELECT año, exportaciones, importaciones, (exportaciones - importaciones) AS saldo_comercial FROM balanza_comercial"
        }
    },
    "V10_PIB_Real": {
        "label": "PIB Real y Crecimiento (V10)",
        "excel_name": "V10_PIB_Real.xlsx",
        "tables": {
            "PIB_Real_Gasto": "SELECT * FROM PIB_Real_Gasto",
            "Tasa_Crecimiento_PIB": "SELECT * FROM Tasa_Crecimiento_PIB"
        }
    },
    "V11_Tasa_de_Inflacion": {
        "label": "Tasa de Inflación - IPC (V11)",
        "excel_name": "V11_Tasa_de_Inflacion.xlsx",
        "tables": {
            "poder_adquisitivo_coste_vida": "SELECT * FROM poder_adquisitivo_coste_vida",
            "inflacion_acumulada": "SELECT * FROM inflacion_acumulada"
        }
    }
}

def exportar_tablas_variables():
    print("=" * 75)
    print("🚀 INICIANDO EXPORTACIÓN ESTRUCTURADA DE VARIABLES A EXCEL (PDF MAPPING)")
    print("=" * 75)
    
    if not DB_PATH.exists():
        print(f"❌ Error: No se encontró la base de datos en {DB_PATH.resolve()}")
        sys.exit(1)
        
    conn = sqlite3.connect(DB_PATH)
    
    # Ensure output directory exists
    OUTPUT_BASE_DIR.mkdir(parents=True, exist_ok=True)
    
    stats = {
        "success": 0,
        "failed": 0,
        "variables_processed": 0
    }
    
    for var_key, config in VARIABLES_CONFIG.items():
        label = config["label"]
        excel_name = config["excel_name"]
        tables_queries = config["tables"]
        
        # Create directory for the variable
        var_dir = OUTPUT_BASE_DIR / var_key
        var_dir.mkdir(parents=True, exist_ok=True)
        
        excel_path = var_dir / excel_name
        
        print(f"\n📦 Procesando Variable: {label}")
        print(f"   📂 Carpeta: {var_dir.relative_to(var_dir.parent.parent)}")
        print(f"   📄 Archivo: {excel_name}")
        
        try:
            # We use pd.ExcelWriter to export multiple tables as sheets
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                has_data = False
                for sheet_name, query in tables_queries.items():
                    print(f"      🔍 Consultando tabla/consulta '{sheet_name}'...")
                    try:
                        df = pd.read_sql(query, conn)
                        if not df.empty:
                            # Excel sheets are limited to 31 characters, so we truncate to 30
                            short_sheet_name = sheet_name[:30]
                            df.to_excel(writer, sheet_name=short_sheet_name, index=False)
                            print(f"      ✅ Hoja '{short_sheet_name}' exportada con {len(df)} registros.")
                            has_data = True
                        else:
                            print(f"      ⚠️ La tabla/consulta '{sheet_name}' está vacía. Saltando...")
                    except Exception as tbl_err:
                        print(f"      ❌ Error al consultar la tabla '{sheet_name}': {tbl_err}")
                
            if has_data:
                print(f"   ✓ Excel de variable creado con éxito.")
                stats["success"] += 1
            else:
                print(f"   ⚠️ No se exportó ningún dato para la variable {var_key}.")
                # Remove empty excel if created
                if excel_path.exists():
                    excel_path.unlink()
                stats["failed"] += 1
                
        except Exception as exc_err:
            print(f"   ❌ Error al crear el archivo Excel para {var_key}: {exc_err}")
            stats["failed"] += 1
            
        stats["variables_processed"] += 1
        
    conn.close()
    
    print("\n" + "=" * 75)
    print("📊 RESUMEN DE EXPORTACIÓN")
    print("=" * 75)
    print(f"✅ Variables exitosas: {stats['success']}")
    print(f"❌ Variables fallidas:  {stats['failed']}")
    print(f"📋 Total procesadas:    {stats['variables_processed']}")
    print(f"📂 Carpeta de salida:   {OUTPUT_BASE_DIR.resolve()}")
    print("=" * 75)

if __name__ == "__main__":
    exportar_tablas_variables()
