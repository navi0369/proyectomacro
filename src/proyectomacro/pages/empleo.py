# src/proyectomacro/pages/empleo.py
import dash
from dash import html

dash.register_page(__name__, name="Empleo", path="/empleo")

layout = html.Div([
    html.H3("Empleo"),
])
