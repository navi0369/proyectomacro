# src/proyectomacro/pages/cuentas_nacionales/pib_ramas.py
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
    path="/cuentas-nacionales/pib-ramas",
    name="PIB por ramas",
    title="PIB por ramas de actividad",
    metadata={"section": "Cuentas Nacionales"},
)

TABLE_ID = "pib_ramas"

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

# Metadatos usando la función auxiliar (recomendado)
metadata = create_metadata_helper(
    nombre_descriptivo="Desagregación del PIB por sectores económicos",
    periodo="1950–2022",
    unidades={
        "PIB Total": "Miles de bolivianos constantes de 1990",
        "Agricultura": "Miles de bolivianos constantes de 1990", 
        "Minería": "Miles de bolivianos constantes de 1990",
        "Industria": "Miles de bolivianos constantes de 1990"
    },
    fuentes=[
        "Instituto Nacional de Estadística (INE) https://track.toggl.com/timer",
        "Banco Central de Bolivia (BCB)",
        "Archivo Excel db/pruebas.xlsx"
    ],
    notas=[
        "Datos preliminares para 2019–2022",
        "Base año 1990 = 100",
        "Incluye revisiones metodológicas 2020"
    ]
)

# Alternativa: Metadatos construidos manualmente
# metadata = {
#     "Nombre descriptivo": "Desagregación del PIB por sectores económicos",
#     "Período": "1950–2022",
#     "Unidad": {
#         "PIB Total": "Miles de bolivianos constantes de 1990",
#         "Agricultura": "Miles de bolivianos constantes de 1990", 
#         "Minería": "Miles de bolivianos constantes de 1990",
#         "Industria": "Miles de bolivianos constantes de 1990"
#     },
#     "Fuente": [
#         "Instituto Nacional de Estadística (INE)",
#         "Banco Central de Bolivia (BCB)",
#         "Archivo Excel db/pruebas.xlsx"
#     ],
#     "Notas": [
#         "Datos preliminares para 2019–2022",
#         "Base año 1990 = 100",
#         "Incluye revisiones metodológicas 2020"
#     ],
#     "Estado de validación": "✅ OK",
# }

 
# ──────────────────────────────────────────────────────────────────────
# 3. Layout final
# ──────────────────────────────────────────────────────────────────────
layout = dbc.Container([
    build_breadcrumb(
        crumbs=[
            {"label": "Inicio", "href": "/"},
            {"label": "Cuentas Nacionales", "href": "/cuentas-nacionales"},
            {"label": "PIB por ramas", "active": True},
        ],
        status=metadata["Estado de validación"],
        badge_success_marker="✅"
    ),

    # 2. header
    build_header(
        title="PIB por ramas de actividad",
        desc=metadata["Nombre descriptivo"],
        metadata=metadata
    ),

    # C. Alerta si hubo error de carga
    dbc.Alert(f"Error cargando datos: {load_error}", color="danger") if load_error else None,


    # E. Galería de imágenes
    build_image_gallery_card(
        groups=images,       # dict {"Serie completa": [...], "Crisis": [...]}
        table_id=TABLE_ID,   # "pib_ramas"
        title="Galería de imágenes",
        initially_open=False,
        toggle_id="btn-toggle-img",
        collapse_id="img-panel",
    ),
    # D. KPI + Tabla
    # build_kpi_cards(df),
    build_data_table(df, TABLE_ID, table_styles, page_size=10),
    # G. Footer
    html.Hr(),
    html.Small("Fuente original: Archivo Excel db/pruebas.xlsx – Última validación 2025-07-31"),

], fluid=True, className="pt-2")

# ──────────────────────────────────────────────────────────────────────
# 4. Callbacks
# ──────────────────────────────────────────────────────────────────────
@callback(
    Output("meta-panel", "is_open"),
    Input("btn-toggle-meta", "n_clicks"),
    State("meta-panel", "is_open"),
    prevent_initial_call=True,
)
def toggle_meta(n_clicks, is_open):
    return not is_open
@callback(
    Output("img-panel", "is_open"),
    Input("btn-toggle-img", "n_clicks"),
    State("img-panel", "is_open"),
    prevent_initial_call=True,
)
def toggle_images(n, is_open):
    return not is_open