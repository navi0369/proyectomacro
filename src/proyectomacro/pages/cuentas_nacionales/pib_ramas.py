# src/proyectomacro/pages/cuentas_nacionales/pib_ramas.py
import dash
from dash import html, dcc, dash_table, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from proyectomacro.extract_data import list_table_image_groups
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
def build_metadata_panel(meta: dict) -> dbc.Card:
    rows = [
        dbc.Row(
            [dbc.Col(html.Small(f"{k}:"), width=4),
             dbc.Col(html.Small(v),       width=8)],
            className="mb-1"
        )
        for k, v in meta.items()
    ]
    return dbc.Card(dbc.CardBody(rows), className="mt-2")


def build_kpi_cards(df_: pd.DataFrame) -> html.Div:
    if df_.empty:
        return dbc.Alert("No hay datos para calcular KPIs.", color="warning")

    latest_year = df_.index.max()
    prev_year   = latest_year - 1

    def safe_val(year, col):
        return df_.loc[year, col] if year in df_.index and col in df_.columns else np.nan

    pib_real_latest = safe_val(latest_year, "pib_real")
    pib_real_prev   = safe_val(prev_year,  "pib_real")
    growth = (
        (pib_real_latest - pib_real_prev) / pib_real_prev * 100
        if pib_real_prev not in (0, np.nan) else np.nan
    )

    cards = dbc.Row(
        [
            dbc.Card(
                dbc.CardBody([
                    html.H6("PIB real (último año)", className="card-title"),
                    html.H4(f"{pib_real_latest:,.2f}", className="mb-0"),
                    html.Small(f"Año {latest_year}")
                ]),
                className="me-2",
                style={"flex": "1"}
            ),
            dbc.Card(
                dbc.CardBody([
                    html.H6("Crecimiento anual PIB real", className="card-title"),
                    html.H4(f"{growth:.2f} %", className="mb-0" if not np.isnan(growth) else "text-muted"),
                    html.Small(f"{prev_year} → {latest_year}")
                ]),
                style={"flex": "1"}
            ),
        ],
        className="g-2 mb-3",
        style={"display": "flex"}
    )
    return cards


def build_image_gallery(groups: dict[str, list[str]]):
    """Devuelve Tabs donde cada pestaña muestra las imágenes en grande con botón Descargar."""
    tabs = []
    for label, imgs in groups.items():
        if not imgs:
            content = html.P("No hay imágenes disponibles.", className="text-muted")
        else:
            rows = []
            for img in imgs:
                folder = "serie_completa" if label == "Serie completa" else "crisis"
                asset_path = f"{folder}/{TABLE_ID}/{img}"
                src = dash.get_asset_url(asset_path)

                rows.append(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(
                                    src=src,
                                    alt=f"{label} – {img}",
                                    className="img-fluid rounded shadow-sm mb-2",
                                ),
                                width=12,
                            ),
                            dbc.Col(
                                html.A(
                                    "Descargar",
                                    href=src,
                                    download=img,
                                    target="_blank",
                                    className="btn btn-primary mb-4",
                                ),
                                width="auto",
                            ),
                        ],
                        className="align-items-center",
                    )
                )
            content = html.Div(rows)
        tabs.append(dbc.Tab(content, label=label))
    return dbc.Tabs(tabs, id="img-tabs", className="mb-3")


# ──────────────────────────────────────────────────────────────────────
# 3. Layout final
# ──────────────────────────────────────────────────────────────────────
layout = dbc.Container([
    # A. Encabezado
    dbc.Row([
        dbc.Col(
            dbc.Breadcrumb(items=[
                {"label": "Inicio",               "href": "/"},
                {"label": "Cuentas Nacionales",   "href": "/cuentas-nacionales"},
                {"label": "PIB por ramas",        "active": True},
            ]),
            md=8
        ),
        dbc.Col(
            html.Span(metadata["Estado de validación"], className="badge bg-success"),
            md=4, style={"textAlign": "right"}
        ),
    ], align="center", className="mb-1"),

    # B. Título, subtítulo y metadatos
    html.H2("PIB por ramas de actividad"),
    html.P(metadata["Nombre descriptivo"]),
    dbc.Button("Mostrar detalles de la tabla", id="btn-toggle-meta", color="link", className="p-0 mb-1"),
    dbc.Collapse(build_metadata_panel(metadata), id="meta-panel", is_open=False),

    # C. Alerta si hubo error de carga
    dbc.Alert(f"Error cargando datos: {load_error}", color="danger") if load_error else None,


    # E. Galería de imágenes
    dbc.Card([
        dbc.CardHeader("Galería de imágenes"),
        dbc.CardBody(build_image_gallery(images)),
    ], className="my-4 shadow-sm"),
    # D. KPI + Tabla
    build_kpi_cards(df),
    dash_table.DataTable(
        id="pib-table",
        data=df.reset_index().to_dict("records") if not df.empty else [],
        columns=[{"name": c, "id": c} for c in df.reset_index().columns] if not df.empty else [],
        page_size=10,
        page_action="native",
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        export_format="csv",
        export_headers="display",
        virtualization=True,
        fixed_rows={"headers": True},
        tooltip_data=[
            {c: {"value": str(v), "type": "text"} for c, v in row.items()}
            for row in df.reset_index().to_dict("records")
        ] if not df.empty else [],
        tooltip_duration=None,
        **table_styles,
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "#f1f3f5"},  # zebra
        ],
        style_cell_conditional=[
            {"if": {"column_id": "año"}, "textAlign": "left", "fontWeight": "600"},
        ],
    ),
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
