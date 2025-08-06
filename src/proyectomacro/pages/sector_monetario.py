# src/proyectomacro/pages/sector_monetario.py
import dash
from dash import html

dash.register_page(__name__, name="Sector Monetario", path="/sector-monetario")

layout = html.Div([
    html.H3("Sector Monetario"),
])
