# src/proyectomacro/pages/cuentas_nacionales/pib_ramas.py
import dash
from dash import html, dcc, dash_table, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from proyectomacro.extract_data import list_table_image_groups
from proyectomacro.page_utils import build_breadcrumb, build_header, build_image_gallery_card, build_data_table, create_metadata_helper, load_metadata_from_config, get_table_styles
from func_auxiliares.graficos_utils import get_df
from func_auxiliares.config import DB_PATH

from dash import MATCH, ALL
from dash.exceptions import PreventUpdate
import json
from dash import callback_context

# Nota: Los estilos de tabla ahora están centralizados en page_utils.py
# Si necesitas personalizar estilos específicos para esta tabla, usa:
# table_styles = get_table_styles({"style_header": {"backgroundColor": "#custom-color"}})

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

# Metadatos: primero intentar cargar desde configuración YAML
metadata = load_metadata_from_config(TABLE_ID)


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
        metadata=metadata,
        toggle_id=f"{TABLE_ID}-btn-toggle-meta",
        collapse_id=f"{TABLE_ID}-meta-panel"
    ),

    # C. Alerta si hubo error de carga
    dbc.Alert(f"Error cargando datos: {load_error}", color="danger") if load_error else None,


    # E. Galería de imágenes
    build_image_gallery_card(
        groups=images,       # dict {"Serie completa": [...], "Crisis": [...]}
        table_id=TABLE_ID,   # "pib_ramas"
        title="Galería de imágenes",
        initially_open=False,
        toggle_id=f"{TABLE_ID}-btn-toggle-img",
        collapse_id=f"{TABLE_ID}-img-panel",
    ),
    # D. KPI + Tabla
    # build_kpi_cards(df),
    build_data_table(df, TABLE_ID, page_size=10),  # Usa estilos predeterminados
    # G. Footer
    html.Hr(),
    html.Small("Fuente original: Archivo Excel db/pruebas.xlsx – Última validación 2025-07-31"),

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