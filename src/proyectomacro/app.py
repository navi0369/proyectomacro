# src/proyectomacro/app.py
import dash
import dash_bootstrap_components as dbc
from dash import html, page_container, page_registry
from func_auxiliares.config import ASSETS_DIR
########################################################################
# 1. Crear la aplicación y habilitar Dash pages
########################################################################
app = dash.Dash(
    __name__,
    use_pages=True,                       # << activa el enrutamiento nativo 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,     # por si hay callbacks en cada page
    assets_folder=str(ASSETS_DIR),         # carpeta de assets
)
server = app.server

########################################################################
# 2. Construir el sidebar con las SECCIONES PRINCIPALES
#    (Inicio, Cuentas Nacionales, Sector Externo, Precios y Producción,
#     Exportaciones, Importaciones, Sector Fiscal, Deuda, Empleo,
#     Pobreza, Sector Monetario)
########################################################################
SECCIONES = [
    "Inicio",
    "Documentos",
    "Calculadora",
    "Cuentas Nacionales",
    "Sector Externo",
    "Exportaciones",
    "Importaciones",
    "Precios y Producción",
    "Sector Fiscal",
    "Deuda",
    "Empleo",
    "Pobreza",
    "Sector Monetario",
]

nav_links = []
for sec in SECCIONES:
    # Busca en page_registry la página cuyo "name" coincida
    page = next((p for p in page_registry.values() if p["name"] == sec), None)
    if page:
        nav_links.append(
            dbc.NavLink(
                sec,
                href=page["path"],
                active="exact",
                className="my-1",
            )
        )
sidebar = dbc.Nav(
    nav_links,
    vertical=True,
    pills=True,
    className="bg-light p-2 sidebar",
)

########################################################################
# 3. Layout general: Sidebar + Contenedor de página
########################################################################
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H2("Dashboard Macroeconómico de Bolivia"), width=12),
            className="my-3",
        ),
        dbc.Row(
            [
                dbc.Col(sidebar, width=2),
                dbc.Col(page_container, width=10),     # aquí se inyecta cada page
            ],
            className="h-100",
        ),
    ], 
    fluid=True,
)

########################################################################
# 4. Ejecutar la aplicación
########################################################################
if __name__ == "__main__":
    app.run(debug=True)  