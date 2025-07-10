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

import pandas as pd
import matplotlib.pyplot as plt

# Si aún no instalaste el paquete en editable, descomenta la siguiente línea:
# sys.path.append(os.path.abspath('../'))

from func_auxiliares.graficos_utils import (
    get_df, set_style, init_base_plot, add_year_value_annotations
)
from func_auxiliares.config import (
    DB_PATH, ASSETS_DIR,
    PERIODOS_PARA_CRISIS
)

# ─────────────────────────────────────────────────────────────────────
# Configuración general
# ─────────────────────────────────────────────────────────────────────
output_dir = ASSETS_DIR / "crisis" / "reservas_internacionales"
output_dir.mkdir(parents=True, exist_ok=True)

set_style()

# ─────────────────────────────────────────────────────────────────────
# Carga de datos
# ─────────────────────────────────────────────────────────────────────
SQL = """
    SELECT
      año,
      reservas_totales
    FROM Reservas_oro_divisas
"""
df = get_df(SQL, str(DB_PATH), index_col="año")

# ─────────────────────────────────────────────────────────────────────
# Componentes y parámetros de graficado
# ─────────────────────────────────────────────────────────────────────
componentes = [("reservas_totales", "Reservas internacionales")]
cols_componentes = [col for col, _ in componentes]
colors = {"reservas_totales": "#2ca02c"}


annotation_offsets = {
    "reservas_totales": {
        1950: (0,  -1),
        1951: (0.1,  -1),
        1952: (-0.1,  -1),
        1953: (0,  1),
        1954: (0,  1),
        1955: (0,  1),
        1956: (0,  1.2),
        1957: (0,  1),
        1958: (0, -1),  
        1959: (0,  1),
        1960: (0,  -1),


        1980: (0,  3),   
        1981: (0,  -3),
        1982: (-0.3,  -5),
        1983: (0,  -3),
        1984: (0,  3),
        1985: (0,  -3),
        1986: (-0.1,  3),
        1987: (0, 3),   
        1988: (0,  -3),
        1989: (0,  3),
        1990: (0,  -3),

        2014: (-0.2,  -380),  
        2015: (0.3,  320),   
        2016: (0, -260),   
        2017: (0,  300),
        2018: (0.2,  300),
        2019: (0.2,  300),
        2020: (0, -500),
        2021: (0.2,  300),   
        2022: (0.2,  320),
        2023: (0,  -300),   
    }
}

# ─────────────────────────────────────────────────────────────────────
# Generación de gráficas por subperíodo
# ─────────────────────────────────────────────────────────────────────
for nombre, (ini, fin) in PERIODOS_PARA_CRISIS.items():
    sub = df.loc[ini:fin]

    years_to_annot = list(sub.index)
    fig, ax = init_base_plot(
        sub,
        series=componentes,
        colors=colors,
        title=f"RESERVAS INTERNACIONALES ({nombre})",
        xlabel="Año",
        ylabel="Millones USD",
        source_text="Fuente: Banco Mundial / BCB"
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
    fig.savefig(output_dir / f"reservas_{nombre}.png")
    plt.show()  # Mostrar la figura en pantalla
    plt.close(fig)
