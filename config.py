import os

# LLM
MODEL_NAME = "gpt-4o-mini"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Periodos económicos
PERIODOS = [
    ("1952–1985", 1952, 1985),
    ("1985–2006", 1985, 2006),
    ("2006–Final", 2006, None)
]

# 1) Determino la carpeta raíz del proyecto (dos niveles arriba si estás
#    guardando config.py en la raíz; aquí asumimos que config.py está
#    como /…/Proyecto_macro/config.py).

ROOT = os.path.abspath(os.path.dirname(__file__))  
# os.path.dirname(__file__) → /home/navi/.../Proyecto_macro
# abspath lo deja canónico.

DB_PATH = os.path.join(ROOT, "db", "proyectomacro.db")
# eso da "/home/navi/.../Proyecto_macro/db/proyectomacro.db"



# -----------------------------
# Estilos personalizados para Dash
# -----------------------------
table_styles = {
    'style_table': {'overflowX': 'auto'},
    'style_cell': {
        'textAlign': 'center',
        'padding': '8px',
        'minWidth': '100px', 'width': '100px', 'maxWidth': '180px',
        'fontFamily': 'Arial, sans-serif',
        'fontSize': '14px'
    },
    'style_header': {
        'backgroundColor': '#007BFF',
        'fontWeight': 'bold',
        'color': 'white'
    }
}
# Define estilos reutilizables para las tabs
tabs_styles = {
    "display": "flex",
    "flexWrap": "wrap",         # Permite que las pestañas hagan 'salto de línea' si son muchas
    "justifyContent": "center", # Centra las pestañas horizontalmente
    "borderBottom": "1px solid #d6d6d6",
    "backgroundColor": "#f8f9fa",
    "padding": "5px"
}
tab_style = {
    "padding": "10px 20px",
    "margin": "5px",
    "border": "1px solid #d6d6d6",
    "backgroundColor": "#e9ecef",
    "borderRadius": "5px",
    "fontWeight": "bold",
    "cursor": "pointer"
}

# Estilo para la pestaña seleccionada
tab_selected_style = {
    "padding": "10px 20px",
    "margin": "5px",
    "border": "1px solid #007BFF",
    "backgroundColor": "#ffffff",
    "color": "#007BFF",
    "borderRadius": "5px",
    "fontWeight": "bold"
}
#MINERALES
volumen_base = "/assets/imagenes/12.exportaciones_minerales_totales/12.1.volumen_exportado/"
minerals_volumen_info = [
    ("Estaño", "12.1.1.estaño.png", "estaño_volumen.png"),
    ("Plomo", "12.1.2.plomo.png", "plomo_volumen.png"),
    ("Zinc", "12.1.3.zinc.png", "zinc_volumen.png"),
    ("Plata", "12.1.4.plata.png", "plata_volumen.png"),
    ("Wolfram", "12.1.5.wolfram.png", "wolfram_volumen.png"),
    ("Cobre", "12.1.6.cobre.png", "cobre_volumen.png"),
    ("Antimonio", "12.1.7.antimonio.png", "antimonio_volumen.png"),
    ("Oro", "12.1.8.oro.png", "oro_volumen.png"),
]
# Información de cada mineral para Valor (ruta base para valor)
valor_base = "/assets/imagenes/12.exportaciones_minerales_totales/12.2.valor_exportado/"
minerals_valor_info = [
    ("Estaño", "12.2.1.estaño_valor.png", "estaño_valor.png"),
    ("Plomo", "12.2.2.plomo_valor.png", "plomo_valor.png"),
    ("Zinc", "12.2.3.zinc_valor.png", "zinc_valor.png"),
    ("Plata", "12.2.4.plata_valor.png", "plata_valor.png"),
    ("Wolfram", "12.2.5.wolfram_valor.png", "wolfram_valor.png"),
    ("Cobre", "12.2.6.cobre_valor.png", "cobre_valor.png"),
    ("Antimonio", "12.2.7.antimonio_valor.png", "antimonio_valor.png"),
    ("Oro", "12.2.8.oro_valor.png", "oro_valor.png"),
]