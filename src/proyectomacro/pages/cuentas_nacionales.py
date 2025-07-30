# src/proyectomacro/pages/cuentas_nacionales.py
import dash_bootstrap_components as dbc
from dash import register_page, html
from extract_data import load_validated_tables

register_page(
    __name__,
    path="/cuentas-nacionales",
    name="Cuentas Nacionales",
)

# Carga data (opcional aquí, útil si quieres mostrar counts u otras métricas)
dfs = load_validated_tables()

# Tablas de la sección
TABLAS = [
    "pib_ramas",
    "participacion_x_m_pib",
    "tasa_crecimiento_pib",
    "participacion_pib_ramas",
    "pib_nominal_gasto",
    "deflactor_implicito_pib_gasto",
    "oferta_total",
    "demanda_total",
    "vbp_sector_2006_2014",
]

# Descripciones para mostrar en el card
LABELS = {
    "pib_ramas":                     "1.1 Desagregación del PIB por ramas de actividad",
    "participacion_x_m_pib":         "1.2 Participación X/M en el PIB",
    "tasa_crecimiento_pib":          "1.3 Tasa de Crecimiento Anual del PIB",
    "participacion_pib_ramas":       "1.5 Participación del PIB por ramas de actividad",
    "pib_nominal_gasto":             "1.6 PIB a precios corrientes por tipo de gasto",
    "deflactor_implicito_pib_gasto": "1.7 Deflactor implícito del PIB por tipo de gasto",
    "oferta_total":                  "1.8 Oferta total y componentes",
    "demanda_total":                 "1.9 Demanda total y componentes",
    "vbp_sector_2006_2014":          "1.10 VBP por ramas de actividad económica",
}

# Construye una tarjeta por cada tabla
cards = []
for tbl in TABLAS:
    link = f"/{tbl.replace('_','-')}"
    cards.append(
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H5(LABELS[tbl], className="card-title"),
                            html.P(f"({tbl})", className="text-muted small"),
                            dbc.Button(
                                "Ver detalle ➔",
                                href=link,
                                color="primary",
                                size="sm",
                                className="mt-2"
                            ),
                        ]
                    )
                ],
                class_name="h-100 card-hover shadow-sm",
                style={"cursor": "pointer"}
            ),
            xs=12, sm=6, md=4, lg=4, className="mb-4"
        )
    )

layout = dbc.Container(
    [
        html.H2("Cuentas Nacionales", className="my-4"),
        dbc.Row(cards, class_name="g-4")
    ],
    fluid=True,
)
