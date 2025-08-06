# src/proyectomacro/pages/cuentas_nacionales/pib_ramas.py
import dash
from dash import html, dcc, dash_table, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from proyectomacro.extract_data import list_table_image_groups
from proyectomacro.page_utils import build_breadcrumb, build_header, build_image_gallery_card, build_data_table
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

# Metadatos fijos para el panel colapsable
metadata = {
    "Nombre descriptivo": "Desagregación del PIB por sectores económicos",
    "Período": "1950–2022",
    "Unidad": "Miles de bolivianos constantes de 1990",
    "Fuente": "Archivo Excel db/pruebas.xlsx",
    "Notas": "Datos preliminares para 2019–2022",
    "Última actualización": "2025-07-31",
    "Estado de validación": "✅ OK",
}

# ──────────────────────────────────────────────────────────────────────
# 2. Componentes auxiliares
# ──────────────────────────────────────────────────────────────────────


# def build_kpi_cards(df_: pd.DataFrame) -> html.Div:
#     if df_.empty:
#         return dbc.Alert("No hay datos para calcular KPIs.", color="warning")

#     latest_year = df_.index.max()
#     prev_year   = latest_year - 1

#     def safe_val(year, col):
#         return df_.loc[year, col] if year in df_.index and col in df_.columns else np.nan

#     pib_real_latest = safe_val(latest_year, "pib_real")
#     pib_real_prev   = safe_val(prev_year,  "pib_real")
#     growth = (
#         (pib_real_latest - pib_real_prev) / pib_real_prev * 100
#         if pib_real_prev not in (0, np.nan) else np.nan
#     )

#     cards = dbc.Row(
#         [
#             dbc.Card(
#                 dbc.CardBody([
#                     html.H6("PIB real (último año)", className="card-title"),
#                     html.H4(f"{pib_real_latest:,.2f}", className="mb-0"),
#                     html.Small(f"Año {latest_year}")
#                 ]),
#                 className="me-2",
#                 style={"flex": "1"}
#             ),
#             dbc.Card(
#                 dbc.CardBody([
#                     html.H6("Crecimiento anual PIB real", className="card-title"),
#                     html.H4(f"{growth:.2f} %", className="mb-0" if not np.isnan(growth) else "text-muted"),
#                     html.Small(f"{prev_year} → {latest_year}")
#                 ]),
#                 style={"flex": "1"}
#             ),
#         ],
#         className="g-2 mb-3",
#         style={"display": "flex"}
#     )
#     return cards





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