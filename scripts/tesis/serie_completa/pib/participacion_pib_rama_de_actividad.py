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
from config import DB_PATH
from tesis import apply_mpl_style
apply_mpl_style()

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3, os
import numpy as np
# ── 1. Parámetros y rutas ────────────────────────────────────────────────────
CRISIS_52_55     = slice(1952, 1955)   # Crisis
EXPANSION_56_69  = slice(1956, 1969)   # Expansión
RECESION_70_81   = slice(1970, 1981)   # Recesión
CRISIS_82_85     = slice(1982, 1985)   # Crisis (neoliberal)
EXPANSION_86_99  = slice(1986, 1999)   # Expansión
CRISIS_00_05     = slice(2000, 2005)   # Crisis
ACUMULACION_06_13= slice(2006, 2013)   # Expansión (acumulación)
RECESION_14_23   = slice(2014, 2024)   # Recesión

OUTPUT_DIR = "../../../../assets/tesis/serie_completa/pib"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── 2. Carga de datos ────────────────────────────────────────────────────────
with sqlite3.connect(DB_PATH, uri=True) as conn:
    df = pd.read_sql_query("SELECT * FROM participacion_pib_ramas", conn)

df.set_index("año", inplace=True)

# Columnas a graficar (excluimos minas_canteras_total)
cols = [
    "agropecuario",
    "mineria",
    "petroleo_crudo_y_gas_natural",
    "industria_manufacturera",
    "construcciones",
    "energia",
    "transportes",
    "comercio_finanzas",
    "gobierno_general",
    "propiedad_vivienda",
    "servicios"
]
pct = df[cols]

# ── 3. Estadísticas promedio por periodo ─────────────────────────────────────
avg_crisis_52_55      = pct.loc[CRISIS_52_55].mean()
avg_expansion_56_69   = pct.loc[EXPANSION_56_69].mean()
avg_recesion_70_81    = pct.loc[RECESION_70_81].mean()
avg_crisis_82_85      = pct.loc[CRISIS_82_85].mean()
avg_expansion_86_99   = pct.loc[EXPANSION_86_99].mean()
avg_crisis_00_05      = pct.loc[CRISIS_00_05].mean()
avg_acumulacion_06_13 = pct.loc[ACUMULACION_06_13].mean()
avg_recesion_14_23    = pct.loc[RECESION_14_23].mean()
#offset
hitos_offset = {
    1951: (1, 0.10),
    1955: (3, 0.05),
    1969: (3, 0.05),
    1981: (1, 0.10),
    1985: (3, 0.05),
    1999: (1, 0.10),
    2005: (3, 0.05),
    2014: (3, 0.05)
}

# ── 4. Gráfico stacked-bar ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 7))
pct.plot(kind="bar", stacked=True, ax=ax, width=0.8)

ax.set_ylabel("Participación (%)")
ax.set_xlabel("Año")
ax.set_title("Participación sectorial del PIB 1950-2023",
             fontweight="bold")

# muevo la leyenda fuera del área de gráfico, abajo
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.15),
    ncol=6,            # ajusta según cuántos ítems tengas
    fontsize=10,
    frameon=False
)
fig.subplots_adjust(bottom=0.25)   # expande margen inferior

# construyo un array 0,1,2,… tan largo como df.index
positions = np.arange(len(df.index))
# uso solo cada segunda posición, y como etiqueta el año correspondiente
plt.xticks(positions[::2], df.index[::2], rotation=45)

# ── 4.5 Líneas verticales y texto de hitos ──────────────────────────────────
hitos_v = {
    1951: "Crisis",
    1955: "Expansión",
    1969: "Recesión",
    1981: "Crisis",
    1985: "Expansión",
    1999: "Crisis",
    2005: "Expansión",
    2014: "Recesión"
}
fig.subplots_adjust(right=0.72)

for yr, lbl in hitos_v.items():
    if yr in pct.index:
        idx = pct.index.get_loc(yr)
        y_max=ax.get_ylim()[1]
        ax.axvline(
            x=idx + 0.5, color="gray", ls="--", lw=1.5, zorder=5
        )
        dx,dy=hitos_offset.get(yr,(0,0.5))
        ax.text(
            idx + 0.5+dx,dy, lbl, rotation=0 if lbl=='Expansión' or lbl=='Recesión' else 90, ha="center", va="top",
            fontsize=12, color="black",
            transform=ax.get_xaxis_transform(), clip_on=False,
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="none"),
            zorder=6
        )

# ── 6. Guardar y mostrar ────────────────────────────────────────────────────
plt.tight_layout()
out_path = os.path.join(OUTPUT_DIR, "participacion_pib_ramas.png")
plt.savefig(out_path, dpi=300)
plt.show()

out_path


import seaborn as sns
df_means = pd.DataFrame({
    #"Crisis 52–55":      avg_crisis_52_55,
    "Expansión 56–68":   avg_expansion_56_69,
    "Recesión 70–81":    avg_recesion_70_81,
    #"Crisis 82–85":      avg_crisis_82_85,
    "Expansión 86–99":   avg_expansion_86_99,
    #"Crisis 00–05":      avg_crisis_00_05,
    "Acumulación 06–13": avg_acumulacion_06_13,
    "Recesión 14–23":    avg_recesion_14_23
}).round(1)

# ── 5. Gráfico seaborn (tabla en grises sobrio) ───────────────────────────────
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(
    df_means,
    annot=True, fmt=".1f",
    cmap="Blues",
    cbar=False,
    linewidths=0.5,
    linecolor="lightgray",
    ax=ax
)

ax.set_title(
    "Promedios de participación sectorial del PIB\npor ciclo económico (1952–2023)",
    fontweight='bold', pad=20
)
ax.set_ylabel("Rama de actividad")
ax.set_xlabel("Periodo económico")
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

plt.tight_layout()
out_file = os.path.join(OUTPUT_DIR, "tabla_promedios_ciclos_seaborn.png")
fig.savefig(out_file)
plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3
import os

# ── Parámetros ────────────────────────────────────────────────────────────────
OUTPUT_DIR = "./figuras"
os.makedirs(OUTPUT_DIR, exist_ok=True)
YEARS = slice(2016, 2024)  # 2018–2023 inclusive

# ── Estilo ────────────────────────────────────────────────────────────────────

# ── Carga y filtrado ──────────────────────────────────────────────────────────
with sqlite3.connect(DB_PATH, uri=True) as conn:
    df = pd.read_sql_query("SELECT * FROM participacion_pib_ramas", conn, index_col="año")

# Seleccionar años 2018–2023
df_subset = df.loc[YEARS]

# ── Gráfica con seaborn ───────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 4))
sns.heatmap(
    df_subset,
    annot=True,
    fmt=".1f",
    cmap="Blues",
    cbar=False,
    linewidths=0.5,
    linecolor="lightgray",
    ax=ax
)

ax.set_title("Participación sectorial del PIB (2018–2023)", fontweight="bold", pad=12)
ax.set_ylabel("Año")
ax.set_xlabel("Rama de actividad")
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

# ── Guardar imagen ───────────────────────────────────────────────────────────

plt.show()



