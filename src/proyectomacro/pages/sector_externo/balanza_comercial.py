# src/proyectomacro/pages/sector_externo/balanza_comercial.py
import dash
from dash import html, dcc, dash_table, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from proyectomacro.extract_data import list_table_image_groups
from proyectomacro.page_utils import build_breadcrumb, build_header, build_image_gallery_card, build_data_table, create_metadata_helper
from func_auxiliares.graficos_utils import get_df
from func_auxiliares.config import DB_PATH

from dash import MATCH, ALL
from dash.exceptions import PreventUpdate
import json
from dash import callback_context

table_styles = {
    "style_table": {"overflowX": "auto"},
    "style_cell": {
        "textAlign": "center",
        "padding": "8px",
        "minWidth": "100px",
        "width": "100px",
        "maxWidth": "180px",
        "fontFamily": "Arial, sans-serif",
        "fontSize": "14px",
    },
    "style_header": {
        "backgroundColor": "#007BFF",
        "fontWeight": "bold",
        "color": "white",
    },
}

dash.register_page(
    __name__,
    path="/sector-externo/balanza-comercial",
    name="Balanza Comercial",
    title="Balanza Comercial de Bolivia",
    metadata={"section": "Sector Externo"},
)

TABLE_ID = "balanza_comercial"

# 1. Carga de datos segura ─────────────────────────────────────────────
try:
    df = get_df(f"SELECT * FROM {TABLE_ID}", conn_str=str(DB_PATH))
    if "año" in df.columns:
        df = df.set_index("año").sort_index()
except Exception as e:
    df = pd.DataFrame()
    load_error = str(e)
else:
    load_error = None

images = list_table_image_groups(TABLE_ID) if not df.empty else {"Serie completa": [], "Crisis": []}

# Metadatos para balanza comercial
metadata = create_metadata_helper(
    nombre_descriptivo="Balanza comercial: exportaciones, importaciones y saldo comercial",
    periodo="1952–2023",
    unidades={
        "Exportaciones": "Millones de dólares estadounidenses",
        "Importaciones": "Millones de dólares estadounidenses",
        "Saldo Comercial": "Millones de dólares estadounidenses",
        "Términos de Intercambio": "Índice (base 2005=100)"
    },
    fuentes=[
        "Banco Central de Bolivia (BCB) https://www.bcb.gob.bo",
        "Instituto Nacional de Estadística (INE) https://www.ine.gob.bo",
        "Ministerio de Desarrollo Productivo y Economía Plural"
    ],
    notas=[
        "Datos preliminares para 2022–2023",
        "Exportaciones incluyen reexportaciones",
        "Importaciones CIF (Costo, Seguro y Flete)",
        "Saldo comercial = Exportaciones - Importaciones"
    ]
)

# ──────────────────────────────────────────────────────────────────────
# 3. Layout final
# ──────────────────────────────────────────────────────────────────────
layout = dbc.Container([
    build_breadcrumb(
        crumbs=[
            {"label": "Inicio", "href": "/"},
            {"label": "Sector Externo", "href": "/sector-externo"},
            {"label": "Balanza Comercial", "active": True},
        ],
        status=metadata["Estado de validación"],
        badge_success_marker="✅"
    ),

    # 2. Header
    build_header(
        title="Balanza Comercial",
        desc=metadata["Nombre descriptivo"],
        metadata=metadata,
        toggle_id=f"{TABLE_ID}-btn-toggle-meta",
        collapse_id=f"{TABLE_ID}-meta-panel"
    ),

    # C. Alerta si hubo error de carga
    dbc.Alert(f"Error cargando datos: {load_error}", color="danger") if load_error else None,

    # E. Galería de imágenes
    build_image_gallery_card(
        groups=images,       # dict {"Serie completa": [...], "Crisis": [...]}
        table_id=TABLE_ID,   # "balanza_comercial"
        title="Galería de imágenes",
        initially_open=False,
        toggle_id=f"{TABLE_ID}-btn-toggle-img",
        collapse_id=f"{TABLE_ID}-img-panel",
    ),

    # D. Tabla de datos
    build_data_table(df, TABLE_ID, table_styles, page_size=15),

    # G. Footer
    html.Hr(),
    html.Small("Fuente original: Banco Central de Bolivia, Instituto Nacional de Estadística – Última validación 2025-08-07"),

], fluid=True, className="pt-2")

# ──────────────────────────────────────────────────────────────────────
# 4. Callbacks
# ──────────────────────────────────────────────────────────────────────
@callback(
    Output(f"{TABLE_ID}-meta-panel", "is_open"),
    Input(f"{TABLE_ID}-btn-toggle-meta", "n_clicks"),
    State(f"{TABLE_ID}-meta-panel", "is_open"),
    prevent_initial_call=True,
)
def toggle_meta(n_clicks, is_open):
    return not is_open

@callback(
    Output(f"{TABLE_ID}-img-panel", "is_open"),
    Input(f"{TABLE_ID}-btn-toggle-img", "n_clicks"),
    State(f"{TABLE_ID}-img-panel", "is_open"),
    prevent_initial_call=True,
)
def toggle_images(n, is_open):
    return not is_open
