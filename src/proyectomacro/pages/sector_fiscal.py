# src/proyectomacro/pages/sector_fiscal.py
import dash
from dash import html

dash.register_page(__name__, name="Sector Fiscal", path="/sector-fiscal")

layout = html.Div([
    html.H3("Sector Fiscal"),
])
