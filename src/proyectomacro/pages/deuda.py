# src/proyectomacro/pages/deuda.py
import dash
from dash import html

dash.register_page(__name__, name="Deuda", path="/deuda")

layout = html.Div([
    html.H3("Deuda"),
])
