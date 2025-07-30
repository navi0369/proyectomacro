from dash import register_page, html, dash_table
from extract_data import load_validated_tables

register_page(__name__,
    path="/sector-externo",
    name="Sector Externo"
)

dfs = load_validated_tables()
# Lista de tablas de esta sección, hard‑codeada o filtrada por convención
TABLAS = ["pib_real_gasto", "pib_ramas", "participacion_pib",]

layout = html.Div([
    html.H2("Cuentas Nacionales"),
    html.Ul([
        html.Li(html.A(tbl.replace("_"," ").title(),
                       href=f"/{tbl.replace('_','-')}"))
        for tbl in TABLAS
    ])
])
