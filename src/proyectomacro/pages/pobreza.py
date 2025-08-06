# src/proyectomacro/pages/pobreza.py
import dash
from dash import html

dash.register_page(__name__, name="Pobreza", path="/pobreza")

layout = html.Div([
    html.H3("Pobreza"),
])
