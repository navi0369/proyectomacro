# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %%
# ─────────────────────────────────────────────────────────────────────
# Importaciones
# ─────────────────────────────────────────────────────────────────────
import sys, os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
 

from func_auxiliares.graficos_utils import (
    get_df, set_style, init_base_plot, add_year_value_annotations, compute_annot_years
)
from func_auxiliares.config import (
    DB_PATH, ASSETS_DIR,
    PERIODOS_PARA_CRISIS
)

# ─────────────────────────────────────────────────────────────────────
# Configuración general
# ─────────────────────────────────────────────────────────────────────
# Carpeta de salida para las gráficas de importaciones en periodos de crisis
output_dir = ASSETS_DIR / "crisis" / "importaciones"
output_dir.mkdir(parents=True, exist_ok=True)

# Aplica tu estilo corporativo
set_style()

# ─────────────────────────────────────────────────────────────────────
# Carga de datos
# ─────────────────────────────────────────────────────────────────────
SQL = """
    SELECT
      año,
      importaciones
    FROM balanza_comercial
"""
df = get_df(SQL, str(DB_PATH), index_col="año")

# ─────────────────────────────────────────────────────────────────────
# Componentes y parámetros de graficado
# ─────────────────────────────────────────────────────────────────────
componentes = [("importaciones", "Importaciones")]
cols_componentes = [col for col, _ in componentes]
colors = {"importaciones": "red"}


annotation_offsets = {
    "importaciones": {
        1950: (-0.2,  0),
        1951: (0,  1.5),
        1952: (0,  1),
        1953: (0.2,  1),
        1954: (0,  -1.5),
        1955: (0,  1.3),
        1956: (0,  1.3),
        1957: (0,  1.3),
        1958: (-0.2, -1.5),  
        1959: (0,  2),
        1960: (0,  1.3),


        1980: (0,  -10),   
        1981: (0.3,  -20),
        1982: (0.2,  16),
        1983: (0.2,  10),
        1984: (0,  -10),
        1985: (0,  10),
        1986: (0,  -10),
        1987: (0, 10),   
        1988: (0,  -10),
        1989: (0.08,  -10),
        1990: (0.2,  10),

        2014: (0,  150),  
        2015: (0.2,  150),   
        2016: (0, -130),   
        2017: (0,  200),
        2018: (0,  100),
        2019: (0.2,  100),
        2020: (0, -140),   
        2022: (0,  100),
        2023: (0.2,  130),
        2024: (0,  -100),   
    }
}
# ─────────────────────────────────────────────────────────────────────
# Generación de gráficas por subperíodo
# ─────────────────────────────────────────────────────────────────────
for nombre, (ini, fin) in PERIODOS_PARA_CRISIS.items():
    sub = df.loc[ini:fin]
    if sub.empty:
        continue
    #si sub tiene solo 3 datos
    if len(sub) < 3:
        print(f"Subperíodo {nombre} tiene menos de 3 datos, omitiendo.")
        continue
    years_to_annot = list(sub.index)  # Aquí tomas los años directamente del índice del DataFrame
    fig, ax = init_base_plot(
        sub,
        series=componentes,
        colors=colors,
        title=f"Importaciones ({nombre})",
        xlabel="Año",
        ylabel="Millones USD",
        source_text="Fuente: Elaboración propia con datos de la INE",
    )
    add_year_value_annotations(
        ax,
        sub,
        years_to_annot,              # los años que quieres anotar
        cols_componentes,
        annotation_offsets,
        colors,
        arrow_lw=0.5,
    )
    # Guardar la figura con nombre descriptivo
    fig.savefig(output_dir / f"importaciones_{nombre}.png")
    plt.show()  # Mostrar la figura en pantalla
    plt.close(fig)

