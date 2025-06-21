import os

# config.py

#constantes para la primera grafica

CYCLES={
    "Crisis 52-55": slice(1952, 1955),
    "Expansión 56-69": slice(1956, 1969),
    "Recesión 70-81": slice(1970, 1981),
    "Crisis 82-85": slice(1982, 1985),
    "Expansión 86-99": slice(1986, 1999),
    "Crisis 00-05": slice(2000, 2005),
    "Expansión 06-13": slice(2006, 2013),
    "Recesión 14-24": slice(2014, 2024),
}
hitos_v = {
    1952: "Crisis", 1956: "Expansión", 1970: "Recesión",
    1982: "Crisis", 1986: "Expansión", 2000: "Crisis",
    2006: "Expansión", 2014: "Recesión"
}
annot_years = [1952,1956,1970,1982, 1986, 2000, 2006,2014, 2023]
periodos_tasas=[
    (1956, 1970),
    (1970, 1982),
    (1986, 2000),
    (2000, 2006), 
    (2006, 2014),
    (2014, 2022),
]
#constantes para la segunda grafica
CYCLES_SIN_CRISIS = {
    "Expansión 50-70": slice(1950, 1970),
    "Recesión 71-84":  slice(1971, 1984),
    "Expansión 85-05": slice(1985, 2005),
    "Expansión 06-14": slice(2006, 2014),
    "Recesión 15-24":  slice(2015, 2024),
}
hitos_v_sin_crisis = {
    1950: "Expansion",
    1971: "Recesion",
    1985: "Expansion",
    2005: "Expansion",
    2015: "Recesion"
}
annot_years_sin_crisis = [1950,1971,1985, 2005, 2015,2022]
periodos_tasas_sin_crisis = [
    (1950, 1970),
    (1971, 1984),
    (1985, 2005),
    (2006, 2014),
    (2015,2022)
]
#constantes para la tercera grafica
CYCLES_PERIODOS= {
    "Intervensionismo-estatal 50-84":   slice(1950, 1984),
    "Neoliberalismo 85-05":   slice(1985, 2005),
    "Neodesarrollismo 06-24":   slice(2006, 2024),
} 
#hitos verticales hitos por periodo
hitos_v_periodos = {
    1950: "1950-1984",
    1985: "1985-2005",
    2006: "2006-2022",
}
annot_years_periodos = [1950,1985,2006,2022]
#anotaciones de tasas con crisis
periodos_tasas_periodos = [
    (1950, 1984)
    (1985, 2005),
    (2006, 2022)
]