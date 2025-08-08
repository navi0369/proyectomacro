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
    get_df, set_style, init_base_plot,
    add_year_value_annotations
)
from func_auxiliares.config import (
    DB_PATH, ASSETS_DIR,
    PERIODOS_PARA_CRISIS
)

# ─────────────────────────────────────────────────────────────────────
# Configuración general
# ─────────────────────────────────────────────────────────────────────
output_dir = ASSETS_DIR / "crisis" / "cotizacion_dolar_mercado_libre"
output_dir.mkdir(parents=True, exist_ok=True)

set_style()

# ─────────────────────────────────────────────────────────────────────
# Carga de datos
# ─────────────────────────────────────────────────────────────────────
SQL = """
    SELECT
      año,
      valor
    FROM cotizacion_dolar_mercado_libre
"""
df = get_df(SQL, str(DB_PATH), index_col="año")

# ─────────────────────────────────────────────────────────────────────
# Componentes y parámetros de graficado
# ─────────────────────────────────────────────────────────────────────
componentes = [
    ("valor", "Cotización Bs/USD")
]
cols_componentes = [col for col, _ in componentes]
colors = {
    "valor": "#9467bd"
}

# offsets de anotaciones (dx, dy) — ajústalos según convenga
annotation_offsets = {
    "valor": {
        1950: (0,  200),
        1951: (0,  300),
        1952: (0,  300),
        1953: (0,  300),
        1954: (-0.3,  200),
        1955: (-0.3,  200),
        1956: (0.24,  -260),
        1957: (0.1,  -350),
        1958: (0, 270),  
        1959: (0,  -270),
        1960: (0,  250),
    }
}

# ─────────────────────────────────────────────────────────────────────
# Generación de gráfica por subperíodo
# ─────────────────────────────────────────────────────────────────────
for nombre, (ini, fin) in PERIODOS_PARA_CRISIS.items():
    sub = df.loc[ini:fin]
    if sub.empty or len(sub) < 3:
        continue

    years_to_annot = list(sub.index)

    fig, ax = init_base_plot(
        sub,
        series=componentes,
        colors=colors,
        title=f"COTIZACION DÓLAR MERCADO LIBRE",
        xlabel="Año",
        ylabel="Bolivianos por USD",
        source_text="Fuente: Recopilación propia con datos de memorias de la economia Boliviana"
    )

    add_year_value_annotations(
        ax,
        sub,
        years_to_annot,
        cols_componentes,
        annotation_offsets,
        colors,
        arrow_lw=0.5
    )

    fig.savefig(output_dir / f"cotizacion_dolar_{nombre}.png")
    plt.show()
    plt.close(fig)


# %%
