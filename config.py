import os
from pathlib import Path

#  ── Raíz del proyecto (donde está la carpeta db/, assets/, mi_paquete/, notebooks/, etc.)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

#  ── Ruta a la base de datos
DB_PATH = PROJECT_ROOT / "db" / "proyectomacro.db"

#  ── Carpeta base de salida de gráficas
ASSETS_DIR = PROJECT_ROOT / "assets" / "tesis"
# config.py
CYCLES_PARA_CRISIS = {
    "Crisis 50-58": slice(1950, 1960),
    "crisis 78-86": slice(1980, 1990),
    "Crisis 2022-2025": slice(2014, 2024)
}
CYCLES={
    "Crisis 52-55": slice(1952, 1955),
    "Expansión 56-69": slice(1956, 1969),
    "Recesión 70-81": slice(1970, 1981),
    "Crisis 82-84": slice(1982, 1984),
    "Expansión 85-00": slice(1985, 2000),
    "Transicion 01-05": slice(2001, 2005),
    "Expansión 06-14": slice(2006, 2014),
    "Recesión 15-24": slice(2015, 2024),
}
hitos_v = {
    1952: "Crisis", 1956: "Expansión", 1970: "Recesión",
    1982: "Crisis", 1985: "Expansión", 2001: "Transición",
    2006: "Expansión", 2014: "Recesión"
}
annot_years = [1952,1956,1970,1982, 1985, 2001, 2006,2014, 2023]
periodos_tasas=[
    (1952, 1955),
    (1956, 1969),
    (1970, 1981),
    (1982, 1984),
    (1985, 2000),
    (2001, 2005), 
    (2006, 2014),
    (2015, 2022),
]
#constantes para la segunda grafica
CYCLES_SIN_CRISIS = {
    "Expansión 56-69": slice(1952, 1969),
    "Recesión 70-84":  slice(1970, 1984),
    "Expansión 85-05": slice(1985, 2005),
    "Expansión 06-14": slice(2006, 2014),
    "Recesión 15-24":  slice(2015, 2024),
}
hitos_v_sin_crisis = {
    1956: "Expansion",
    1970: "Recesion",
    1985: "Expansion",
    2006: "Expansion",
    2014: "Recesion"
}
annot_years_sin_crisis = [1950,1956,1970,1985, 2006, 2014,2022]
periodos_tasas_sin_crisis = [
    (1956, 1969),
    (1970, 1984),
    (1985, 2005),
    (2006, 2014),
    (2015,2022)
]
#constantes para la tercera grafica
CYCLES_PERIODOS= {
    "Intervensionismo-estatal 52-84":   slice(1952, 1984),
    "Neoliberalismo 85-05":   slice(1985, 2005),
    "Neodesarrollismo 06-24":   slice(2006, 2024),
} 
#hitos verticales hitos por periodo
hitos_v_periodos = {
    1952: "Intervensionismo-estatal",
    1985: "Neoliberalismo",
    2006: "Neodesarrollismo",
}
annot_years_periodos = [1952,1985,2006,2022]
#anotaciones de tasas con crisis
periodos_tasas_periodos = [
    (1952, 1984),
    (1985, 2005),
    (2006, 2022)
] 
# LLM
MODEL_NAME = "gpt-4o-mini"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Periodos económicos
PERIODOS = [
    ("1952–1985", 1952, 1985),
    ("1985–2006", 1985, 2006),
    ("2006–Final", 2006, None)
]

# Ruta a base de datos
DB_PATH = "file:db/proyectomacro.db?mode=ro"


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