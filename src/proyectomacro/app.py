# src/proyectomacro/app.py
import dash
import dash_bootstrap_components as dbc
from dash import html, page_container, page_registry, dcc, Input, Output, State
import os
import sys
from func_auxiliares.config import ASSETS_DIR

########################################################################
# 1. Crear la aplicación y habilitar Dash pages
########################################################################
app = dash.Dash(
    __name__,
    use_pages=True,                       # << activa el enrutamiento nativo 
    external_stylesheets=[dbc.themes.BOOTSTRAP],  # Tema claro por defecto
    suppress_callback_exceptions=True,     # por si hay callbacks en cada page
    assets_folder=str(ASSETS_DIR),         # carpeta de assets
)
server = app.server

# Contraseña simple para acceso al dashboard
PASSWORD = "macro2024"  # Cambia esto a la contraseña que prefieras

########################################################################
# 2. Construir el sidebar con las SECCIONES PRINCIPALES
#    (Inicio, Cuentas Nacionales, Sector Externo, Precios y Producción,
#     Exportaciones, Importaciones, Sector Fiscal, Deuda, Empleo,
#     Pobreza, Sector Monetario)
########################################################################
SECCIONES = [
    "Inicio",
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
    className="bg-light p-2 sidebar",  # bg-light por defecto
    id="sidebar-nav",
)

########################################################################
# 3. Layout general: Login + Dashboard
########################################################################
# Componente de login
login_layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(html.H3("Dashboard Macroeconómico de Bolivia")),
                        dbc.CardBody(
                            [
                                html.H5("Acceso Restringido", className="text-center mb-4"),
                                dbc.Input(
                                    id="password-input",
                                    type="password",
                                    placeholder="Ingrese contraseña",
                                    className="mb-3",
                                ),
                                dbc.Button(
                                    "Ingresar",
                                    id="login-button",
                                    color="primary",
                                    className="w-100 mb-2",
                                ),
                                html.Div(id="login-alert"),
                            ]
                        ),
                    ],
                    className="shadow",
                ),
                width={"size": 4, "offset": 4},
            ),
            className="mt-5",
        )
    ],
    fluid=True,
    id="login-container",
)

# Dashboard principal
dashboard_layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(html.H2("Dashboard Macroeconómico de Bolivia"), width=12),
            ],
            className="my-3",
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(sidebar, width=2, id="sidebar-col"),
                dbc.Col(page_container, width=10, id="content-col"),     # aquí se inyecta cada page
            ],
            className="h-100",
        ),
    ], 
    fluid=True,
    id="dashboard-container",
    style={"display": "none"},  # Oculto por defecto
)

# Layout principal con ambos componentes y store para sesión
app.layout = html.Div(
    [
        dcc.Store(id="session-store", storage_type="session"),
        login_layout,
        dashboard_layout,
    ],
    id="main-container",
)

########################################################################
# 4. Callbacks para autenticación y tema
########################################################################
@app.callback(
    [
        Output("session-store", "data"),
        Output("login-alert", "children"),
    ],
    Input("login-button", "n_clicks"),
    State("password-input", "value"),
    prevent_initial_call=True,
)
def validate_password(n_clicks, password):
    """Valida la contraseña ingresada"""
    if password == PASSWORD:
        return {"authenticated": True}, dbc.Alert(
            "¡Acceso concedido!", color="success", dismissable=True
        )
    else:
        return {"authenticated": False}, dbc.Alert(
            "Contraseña incorrecta. Intente nuevamente.", color="danger", dismissable=True
        )


@app.callback(
    [
        Output("login-container", "style"),
        Output("dashboard-container", "style"),
    ],
    Input("session-store", "data"),
)
def toggle_login_dashboard(session_data):
    """Muestra el dashboard si está autenticado, caso contrario muestra login"""
    if session_data and session_data.get("authenticated"):
        return {"display": "none"}, {"display": "block"}
    return {"display": "block"}, {"display": "none"}


## Modo nocturno eliminado: no se manejan estilos dinámicos


########################################################################
# 5. Ejecutar la aplicación
########################################################################
if __name__ == "__main__":
    app.run(debug=True)  