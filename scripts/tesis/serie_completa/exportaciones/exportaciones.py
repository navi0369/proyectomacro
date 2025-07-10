# ---
# jupyter:
#   jupytext:
#     formats: notebooks/tesis/serie_completa///ipynb,scripts/tesis/serie_completa///py:percent
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
# ───────────────────────────── 0. IMPORTS Y CONFIGURACIÓN GLOBAL ─────────────────────────────
import os, sys, sqlite3
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath('../'))                 # utilidades propias
from graficos_utils import *
from config import *                                   # CYCLES, hitos_v, annot_years, periodos_tasas …

OUTPUT_DIR = f"../../../../assets/tesis/serie_completa/exportaciones"
os.makedirs(OUTPUT_DIR, exist_ok=True)

set_style()                                            # estilo uniforme de toda la tesis

# ───────────────────────────── 1. CARGA DE DATOS ─────────────────────────────
with sqlite3.connect("../../../../db/proyectomacro.db") as conn:
    df = (pd.read_sql("SELECT * FROM exportaciones_tradicionales_no_tradicionales", conn)
            .set_index("año")
            .sort_index())

df["exportaciones"] = df["tradicionales"] + df["no_tradicionales"]

# ──────────────── 2. DEFINICIÓN DE COMPONENTES, COLORES Y ABREVIATURAS ────────────────
componentes = [
    ("tradicionales",    "Tradicionales"),
    ("no_tradicionales", "No tradicionales"),
    ("exportaciones",    "Total exportaciones"),
]
cols_componentes = [c for c, _ in componentes]

cmap   = plt.get_cmap("tab10")
colors = {col: cmap(i) for i, (col, _) in enumerate(componentes)}
abbr   = {"tradicionales":"Trad", "no_tradicionales":"NoTrad", "exportaciones":"X"}

# ──────────────── 3. PREPARACIÓN DE CICLOS, ANOTACIONES Y PERÍODOS ────────────────
cycles        = adjust_cycles(df, CYCLES)                       # de config.py
annot_years   = adjust_annot_years(df, annot_years)  # de config.py
annot_years.append(2022)
periodos      = adjust_periods(df, periodos_tasas)              # para growth-arrows
cycle_stats   = {n: df.loc[slice_, cols_componentes].mean().to_dict()
                 for n, slice_ in cycles.items()}

# ──────────────── 4. OFFSETS Y POSICIONAMIENTOS ────────────────
hitos_offsets = {a:0.80 for a in hitos_v}

annotation_offsets = {
    "exportaciones": {
        1982: (0, 800),
        1985: (0, 800),
        2001: (0, 800),
        2006: (0, 1000),
        2014: (-0.5, 400),
        2022: (0, 400),
        2024: (0, -400),
    },
    "tradicionales": {
        1982: (0, 400),
        1985: (0, 400),
        2001: (0, 900),
        2006: (0, -1500),
        2014: (-1, -1800),
        2022: (0, 200),
        2024: (0, -400),
    },
    "no_tradicionales": {
        1982: (0, -350),
        1985: (0, -350),
        2001: (0, -450),
        2006: (0, -500),
        2014: (0, -700),
        2022: (0, 200),
        2024: (0, -500),
    },
}

medias_offsets = {
    "Expansión 85-00":  (1989, 1.05),
    "Expansión 06-14":  (2006, 1.05),
    "Recesión 15-24":   (2015, 1.05),
}

tasas_offsets = {
    "1985-2000": (1989, 0.91),
    "2006-2014": (2006, 0.91),
    "2015-2024": (2015, 0.91),
}

participation_offsets = {
    "1985-2000": (1989, 0.77),
    "2006-2014": (2006, 0.77),
    "2015-2024": (2015, 0.77),
}

# ───────────────────────────── 5. GENERACIÓN DE LA GRÁFICA ─────────────────────────────
fig, ax = init_base_plot(
    df=df,
    series=componentes,                # helper mantiene arg. 'series', recibe la lista componentes
    colors=colors,
    title=f"Exportaciones Tradicionales vs. No Tradicionales ({df.index[0]}–{df.index[-1]})",
    xlabel="Año",
    ylabel="Millones de dólares (USD)",
    source_text="Fuente: Base Proyectomacro",
    legend_ncol=1
)

add_hitos(ax, df.index, hitos_v, hitos_offsets, line_kwargs={"linewidth":0.9})

# medias de ciclo
add_cycle_means_multi(
    ax, cycle_stats, medias_offsets,
    abbr, colors, line_spacing=ax.get_ylim()[1]*0.03
)

# anotaciones puntuales
add_year_value_annotations(
    ax, df, annot_years,
    cols_componentes, annotation_offsets, colors, arrow_lw=0.5
)

# tasas de crecimiento por periodo
add_period_growth_annotations_multi(
    ax, df, periodos,
    cols_componentes, tasas_offsets, colors, abbr
)

# cuadros de participación
add_participation_cycle_boxes(
    ax, df, periodos,
    ["tradicionales","no_tradicionales"],      # componentes parciales
    "exportaciones",                           # total
    participation_offsets,
    abbr_map=abbr, colors={c:colors[c] for c in ["tradicionales","no_tradicionales"]}
)

ax.set_ylim(-600, ax.get_ylim()[1] + 1000)


plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "exportaciones_tradicionales_no_tradicionales.png"), dpi=300)
plt.show()


