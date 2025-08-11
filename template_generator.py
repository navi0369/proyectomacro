# template_generator.py
"""
Generador de templates para páginas de tablas basado en pib_ramas.py
"""

def generate_page_template(table_id, path, title, section_name, section_path):
    """
    Genera el contenido de una página basado en el template de pib_ramas.py
    """
    
    # Convertir table_id de snake_case a kebab-case para URLs
    kebab_path = table_id.replace('_', '-')
    
    template = f'''# src/proyectomacro/pages/{section_name.lower().replace(' ', '_')}/{table_id}.py
import dash
from dash import html, dcc, dash_table, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

from proyectomacro.extract_data import list_table_image_groups
from proyectomacro.page_utils import build_breadcrumb, build_header, build_image_gallery_card, build_data_table, load_metadata_from_config
from func_auxiliares.graficos_utils import get_df
from func_auxiliares.config import DB_PATH

from dash import MATCH, ALL
from dash.exceptions import PreventUpdate
import json
from dash import callback_context

# Nota: Los estilos de tabla ahora están centralizados en page_utils.py
# Si necesitas personalizar estilos específicos para esta tabla, usa:
# from proyectomacro.page_utils import get_table_styles
# table_styles = get_table_styles({{"style_header": {{"backgroundColor": "#custom-color"}}}})

dash.register_page(
    __name__,
    path="{path}/{kebab_path}",
    name="{title}",
    title="{title}",
    metadata={{"section": "{section_name}"}},
)

TABLE_ID = "{table_id}"

# 1. Carga de datos segura ─────────────────────────────────────────────
try:
    df = get_df(f"SELECT * FROM {{TABLE_ID}}", conn_str=str(DB_PATH))
    if "año" in df.columns:
        df = df.set_index("año").sort_index()
except Exception as e:
    df = pd.DataFrame()
    load_error = str(e)
else:
    load_error = None

images = list_table_image_groups(TABLE_ID) if not df.empty else {{"Serie completa": [], "Crisis": []}}

# Metadatos: primero intentar cargar desde configuración YAML
metadata = load_metadata_from_config(TABLE_ID)

# Si no se encuentran en YAML, usar valores por defecto (fallback)
if metadata is None:
    metadata = {{
        "Nombre descriptivo": "{title}",
        "Período": "N/A",
        "Unidad": "N/A",
        "Fuente": ["Pendiente de configuración"],
        "Estado de validación": "⚠️ Sin metadatos",
        "Notas": ["Metadatos pendientes de configuración en pages.yml"]
    }}

# ──────────────────────────────────────────────────────────────────────
# Layout final
# ──────────────────────────────────────────────────────────────────────
layout = dbc.Container([
    build_breadcrumb(
        crumbs=[
            {{"label": "Inicio", "href": "/"}},
            {{"label": "{section_name}", "href": "{section_path}"}},
            {{"label": "{title}", "active": True}},
        ],
        status=metadata["Estado de validación"],
        badge_success_marker="✅"
    ),

    # Header
    build_header(
        title="{title}",
        desc=metadata["Nombre descriptivo"],
        metadata=metadata,
        toggle_id=f"{{TABLE_ID}}-btn-toggle-meta",
        collapse_id=f"{{TABLE_ID}}-meta-panel"
    ),

    # Alerta si hubo error de carga
    dbc.Alert(f"Error cargando datos: {{load_error}}", color="danger") if load_error else None,

    # Galería de imágenes
    build_image_gallery_card(
        groups=images,       # dict {{"Serie completa": [...], "Crisis": [...]}}
        table_id=TABLE_ID,   # "{table_id}"
        title="Galería de imágenes",
        initially_open=False,
        toggle_id=f"{{TABLE_ID}}-btn-toggle-img",
        collapse_id=f"{{TABLE_ID}}-img-panel",
    ),
    
    # Tabla de datos (usa estilos predeterminados)
    build_data_table(df, TABLE_ID, page_size=10),
    
    # Footer
    html.Hr(),
    html.Small(f"Tabla: {{TABLE_ID}} – Última validación pendiente"),

], fluid=True, className="pt-2")

# ──────────────────────────────────────────────────────────────────────
# Callbacks
# ──────────────────────────────────────────────────────────────────────
@callback(
    Output(f"{{TABLE_ID}}-meta-panel", "is_open"),
    Input(f"{{TABLE_ID}}-btn-toggle-meta", "n_clicks"),
    State(f"{{TABLE_ID}}-meta-panel", "is_open"),
    prevent_initial_call=True,
)
def toggle_meta(n_clicks, is_open):
    return not is_open

@callback(
    Output(f"{{TABLE_ID}}-img-panel", "is_open"),
    Input(f"{{TABLE_ID}}-btn-toggle-img", "n_clicks"),
    State(f"{{TABLE_ID}}-img-panel", "is_open"),
    prevent_initial_call=True,
)
def toggle_images(n, is_open):
    return not is_open
'''

    return template

if __name__ == "__main__":
    # Ejemplo de uso
    content = generate_page_template(
        table_id="pib_real_gasto",
        path="/cuentas-nacionales",
        title="PIB real (base 1990) desagregado por componentes de gasto",
        section_name="Cuentas Nacionales",
        section_path="/cuentas-nacionales"
    )
    print(content)
