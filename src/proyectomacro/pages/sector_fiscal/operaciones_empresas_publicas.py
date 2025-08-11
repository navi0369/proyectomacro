# src/proyectomacro/pages/sector_fiscal/operaciones_empresas_publicas.py
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
    path="/sector-fiscal/operaciones-empresas-publicas",
    name="Operaciones de empresas públicas",
    title="Operaciones de empresas públicas",
    metadata={"section": "Sector Fiscal"},
)

TABLE_ID = "operaciones_empresas_publicas"

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

# Metadatos: cargar desde configuración YAML
metadata = load_metadata_from_config(TABLE_ID)

# Si no se encuentran en YAML, usar valores por defecto (fallback)
if metadata is None:
    metadata = {
        "Nombre descriptivo": "Operaciones de empresas públicas",
        "Período": "N/A",
        "Unidad": "N/A",
        "Fuente": ["Pendiente de configuración"],
        "Estado de validación": "⚠️ Sin metadatos",
        "Notas": ["Metadatos pendientes de configuración en pages.yml"]
    }

# ──────────────────────────────────────────────────────────────────────
# Layout final
# ──────────────────────────────────────────────────────────────────────
layout = dbc.Container([
    build_breadcrumb(
        crumbs=[
            {"label": "Inicio", "href": "/"},
            {"label": "Sector Fiscal", "href": "/sector-fiscal"},
            {"label": "Operaciones de empresas públic...", "active": True},
        ],
        status=metadata["Estado de validación"],
        badge_success_marker="✅"
    ),

    # Header
    build_header(
        title="Operaciones de empresas públicas",
        desc=metadata["Nombre descriptivo"],
        metadata=metadata,
        toggle_id=f"{TABLE_ID}-btn-toggle-meta",
        collapse_id=f"{TABLE_ID}-meta-panel"
    ),

    # Alerta si hubo error de carga
    dbc.Alert(f"Error cargando datos: {load_error}", color="danger") if load_error else None,

    # Galería de imágenes
    build_image_gallery_card(
        groups=images,
        table_id=TABLE_ID,
        title="Galería de imágenes",
        initially_open=False,
        toggle_id=f"{TABLE_ID}-btn-toggle-img",
        collapse_id=f"{TABLE_ID}-img-panel",
    ),
    
    # Tabla de datos (usa estilos predeterminados)
    build_data_table(df, TABLE_ID, page_size=10),
    
    # Footer
    html.Hr(),
    html.Small(f"Tabla: {TABLE_ID} – Última validación pendiente"),

], fluid=True, className="pt-2")

# ──────────────────────────────────────────────────────────────────────
# Callbacks
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
