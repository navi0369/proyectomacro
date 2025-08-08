# src/proyectomacro/pages/sector_fiscal.py
import dash
from dash import html
import dash_bootstrap_components as dbc

from proyectomacro.config import load_pages_config
from proyectomacro.page_utils import build_section_cards

dash.register_page(__name__, name="Sector Fiscal", path="/sector-fiscal")

PAGES = load_pages_config()
sec_cfg = PAGES["sector_fiscal"]

tabla_ids = [meta["tabla"] for meta in sec_cfg["tablas"].values()]
labels = {meta["tabla"]: meta["label"] for meta in sec_cfg["tablas"].values()}

layout = dbc.Container([
    html.H2(sec_cfg["name"], className="my-4"),
    build_section_cards(
        tablas=tabla_ids,
        labels=labels,
        base_path=sec_cfg["path"],
    ),
], fluid=True)
