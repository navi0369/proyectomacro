import os
from pathlib import Path

#  ── Raíz del proyecto (donde está la carpeta db/, assets/, mi_paquete/, notebooks/, etc.)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

#  ── Ruta a la base de datos
DB_PATH = PROJECT_ROOT / "db" / "proyectomacro.db"

#  ── Carpeta base de salida de gráficas
ASSETS_DIR = PROJECT_ROOT / "assets" / "tesis"
# config.py

#constantes para la primera grafica
PERIODOS_PARA_CRISIS = {
    "Crisis 50-60": (1950, 1960),
    "crisis 80-90": (1980, 1990),
    "Crisis 14-24": (2014, 2024)
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



#------------------------------------
#constantes para la segunda grafica
#------------------------------------
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




#------------------------------------
#constantes para la tercera grafica
#------------------------------------
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