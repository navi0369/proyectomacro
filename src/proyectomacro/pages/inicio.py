# src/proyectomacro/pages/_inicio.py
from dash import register_page, html

# 1 ▸ Register this file as the root page (“/”)
register_page(
    __name__,
    path="/",              # URL → http://127.0.0.1:8050/
    name="Inicio",         # text that appears in the sidebar
    order=0                # show first if you sort by order
)

# 2 ▸ List of top‑level sections (label, url‑path)
SECCIONES = [
    ("Cuentas Nacionales", "/cuentas-nacionales"),
    ("Sector Externo",     "/sector-externo"),
    ("Exportaciones",      "/exportaciones"),
    ("Importaciones",      "/importaciones"),
    ("Precios y Producción","/precios-produccion"),
    ("Sector Fiscal",      "/sector-fiscal"),
    ("Deuda",              "/deuda"),
    ("Empleo",             "/empleo"),
    ("Pobreza",            "/pobreza"),
    ("Sector Monetario",   "/sector-monetario"),
]

# 3 ▸ Build a flex “card grid” of links
cards = [
    html.Div(
        html.A(label, href=href, className="stretched-link"),
        className="card text-center p-4 m-2 shadow-sm",
        style={"width": "18rem", "minHeight": "6rem", "position": "relative"}
    )
    for label, href in SECCIONES
]

layout = html.Div(
    [
        html.H2("Dashboard Macroeconómico de Bolivia", className="mb-4"),
        html.Div(cards, className="d-flex flex-wrap justify-content-start"),
    ],
    className="p-4",
)