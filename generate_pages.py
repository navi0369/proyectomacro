#!/usr/bin/env python3
"""
Script para generar automáticamente todas las páginas faltantes basándose en pages.yml
"""
import os
import yaml
from pathlib import Path

# Configuración
SRC_DIR = Path("/home/navi/Desktop/archivos/DS/eco/Proyecto_macro/src/proyectomacro")
PAGES_DIR = SRC_DIR / "pages"
CONFIG_FILE = SRC_DIR / "config" / "pages.yml"

def load_config():
    """Carga la configuración desde pages.yml"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_page_content(table_id, table_config, section_name, section_path):
    """Genera el contenido de una página"""
    
    kebab_path = table_id.replace('_', '-')
    actual_table_id = table_config["tabla"]
    label = table_config["label"]
    
    return f'''# src/proyectomacro/pages/{section_name.lower().replace(' ', '_').replace('-', '_')}/{table_id}.py
import dash
from dash import html, dcc, dash_table, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from proyectomacro.extract_data import list_table_image_groups
from proyectomacro.page_utils import build_breadcrumb, build_header, build_image_gallery_card, build_data_table, load_metadata_from_config
from func_auxiliares.graficos_utils import get_df
from func_auxiliares.config import DB_PATH

from dash import MATCH, ALL
from dash.exceptions import PreventUpdate
import json
from dash import callback_context

dash.register_page(
    __name__,
    path="{section_path}/{kebab_path}",
    name="{label}",
    title="{label}",
    metadata={{"section": "{section_name}"}},
)

TABLE_ID = "{actual_table_id}"

# 1. Carga de datos segura ─────────────────────────────────────────────
try:
    df = get_df(f"SELECT * FROM {{TABLE_ID}}", conn_str=str(DB_PATH))
    if "año" in df.columns:
        df = df.set_index("año").sort_index()
except Exception as e:
    df = pd.DataFrame()
    load_error = str(e)
else:
    load_error = None

images = list_table_image_groups(TABLE_ID) if not df.empty else {{"Serie completa": [], "Crisis": []}}

# Metadatos: cargar desde configuración YAML
metadata = load_metadata_from_config(TABLE_ID)

# Si no se encuentran en YAML, usar valores por defecto (fallback)
if metadata is None:
    metadata = {{
        "Nombre descriptivo": "{label}",
        "Período": "N/A",
        "Unidad": "N/A",
        "Fuente": ["Pendiente de configuración"],
        "Estado de validación": "⚠️ Sin metadatos",
        "Notas": ["Metadatos pendientes de configuración en pages.yml"]
    }}

# ──────────────────────────────────────────────────────────────────────
# Layout final
# ──────────────────────────────────────────────────────────────────────
layout = dbc.Container([
    build_breadcrumb(
        crumbs=[
            {{"label": "Inicio", "href": "/"}},
            {{"label": "{section_name}", "href": "{section_path}"}},
            {{"label": "{label[:30]}{'...' if len(label) > 30 else ''}", "active": True}},
        ],
        status=metadata["Estado de validación"],
        badge_success_marker="✅"
    ),

    # Header
    build_header(
        title="{label}",
        desc=metadata["Nombre descriptivo"],
        metadata=metadata,
        toggle_id=f"{{TABLE_ID}}-btn-toggle-meta",
        collapse_id=f"{{TABLE_ID}}-meta-panel"
    ),

    # Alerta si hubo error de carga
    dbc.Alert(f"Error cargando datos: {{load_error}}", color="danger") if load_error else None,

    # Galería de imágenes
    build_image_gallery_card(
        groups=images,
        table_id=TABLE_ID,
        title="Galería de imágenes",
        initially_open=False,
        toggle_id=f"{{TABLE_ID}}-btn-toggle-img",
        collapse_id=f"{{TABLE_ID}}-img-panel",
    ),
    
    # Tabla de datos (usa estilos predeterminados)
    build_data_table(df, TABLE_ID, page_size=10),
    
    # Footer
    html.Hr(),
    html.Small(f"Tabla: {{TABLE_ID}} – Última validación pendiente"),

], fluid=True, className="pt-2")

# ──────────────────────────────────────────────────────────────────────
# Callbacks
# ──────────────────────────────────────────────────────────────────────
@callback(
    Output(f"{{TABLE_ID}}-meta-panel", "is_open"),
    Input(f"{{TABLE_ID}}-btn-toggle-meta", "n_clicks"),
    State(f"{{TABLE_ID}}-meta-panel", "is_open"),
    prevent_initial_call=True,
)
def toggle_meta(n_clicks, is_open):
    return not is_open

@callback(
    Output(f"{{TABLE_ID}}-img-panel", "is_open"),
    Input(f"{{TABLE_ID}}-btn-toggle-img", "n_clicks"),
    State(f"{{TABLE_ID}}-img-panel", "is_open"),
    prevent_initial_call=True,
)
def toggle_images(n, is_open):
    return not is_open
'''

def main():
    """Función principal que genera todas las páginas"""
    
    config = load_config()
    created_files = []
    skipped_files = []
    
    print("🚀 Generando páginas automáticamente desde pages.yml...")
    print("=" * 60)
    
    for section_key, section_data in config["secciones"].items():
        section_name = section_data["name"]
        section_path = section_data["path"]
        
        # Crear directorio de sección si no existe
        section_dir = PAGES_DIR / section_key.replace('-', '_')
        section_dir.mkdir(exist_ok=True)
        
        print(f"📁 Sección: {section_name} ({section_key})")
        
        for table_key, table_config in section_data.get("tablas", {}).items():
            file_path = section_dir / f"{table_key}.py"
            
            # Verificar si el archivo ya existe
            if file_path.exists():
                print(f"   ⚠️  {table_key}.py ya existe - OMITIDO")
                skipped_files.append(str(file_path))
                continue
            
            # Generar contenido de la página
            content = generate_page_content(
                table_key, table_config, section_name, section_path
            )
            
            # Escribir archivo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   ✅ {table_key}.py creado")
            created_files.append(str(file_path))
    
    print("=" * 60)
    print(f"📊 Resumen:")
    print(f"   ✅ Archivos creados: {len(created_files)}")
    print(f"   ⚠️  Archivos omitidos: {len(skipped_files)}")
    
    if created_files:
        print(f"\\n📝 Archivos creados:")
        for file_path in created_files:
            print(f"   - {file_path}")
    
    if skipped_files:
        print(f"\\n⚠️  Archivos omitidos (ya existían):")
        for file_path in skipped_files:
            print(f"   - {file_path}")
    
    print(f"\\n🎉 ¡Generación completada!")

if __name__ == "__main__":
    main()
