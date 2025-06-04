# ---
# jupyter:
#   jupytext:
#     formats: notebooks///ipynb,scripts///py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.2
#   kernelspec:
#     display_name: aider
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3, os

# ── 1. Parámetros y rutas ─────────────────────────────────────────────────────
CRISIS_YEARS = slice(2002, 2006)            # 2002-2005 inclusive
POST_YEARS   = slice(2006, 2024)            # 2006-2023 inclusive
OUTPUT_DIR   = "../../../assets/tesis/neodesarollismo/serie_completa"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── 2. Estilo profesional ─────────────────────────────────────────────────────
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "font.family": "serif", "font.size": 12,
    "axes.titlesize": 16, "axes.labelsize": 14,
    "grid.linestyle": "--", "lines.linewidth": 2,
    "figure.dpi": 150, "savefig.bbox": "tight"
})

# ── 3. Carga de datos ─────────────────────────────────────────────────────────
with sqlite3.connect("../../../db/proyectomacro.db") as conn:
    df = pd.read_sql_query(
        "SELECT * FROM participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos",
        conn
    )

df.set_index("año", inplace=True)
df = df.loc[2002:2023].copy()               # Ajustar hasta 2023

# ── 4. Estadísticas promedio por periodo ──────────────────────────────────────
avg_crisis = df.loc[CRISIS_YEARS].mean()
avg_post   = df.loc[POST_YEARS].mean()

# ── 5. Gráfico stacked-bar ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(15, 7))
df.plot(kind="bar", stacked=True, ax=ax, width=0.8)

ax.set_ylabel("Participación (%)")
ax.set_xlabel("Año")
ax.set_title(
    "Participación de Gas y Otros Hidrocarburos (2002-2023)",
    fontweight="bold"
)
ax.legend(["Gas Natural", "Otros Hidrocarburos"], loc="upper left",
          bbox_to_anchor=(1, 1))
plt.xticks(rotation=45)

# ── 6. Cajas de resumen ────────────────────────────────────────────────────────
stats_crisis = (
    f"Gas Natural:        {avg_crisis['exportacion_gas']:.1f}%\n"
    f"Otros hidrocarburos: {avg_crisis['otros_hidrocarburos']:.1f}%"
)
stats_post = (
    f"Gas Natural:        {avg_post['exportacion_gas']:.1f}%\n"
    f"Otros hidrocarburos: {avg_post['otros_hidrocarburos']:.1f}%"
)

ax.text(1.02, 0.65, "Crisis (2002-05)\n" + stats_crisis,
        transform=ax.transAxes, fontsize=10, va="center", ha="left",
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="black"))
ax.text(1.02, 0.30, "Post-crisis (2006-23)\n" + stats_post,
        transform=ax.transAxes, fontsize=10, va="center", ha="left",
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="black"))

# ── 7. Guardar y mostrar ──────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "participacion_gas_hidrocarburos_2002_2023.png"),
            dpi=300)
plt.show()

# ── 8. Verificación rápida ────────────────────────────────────────────────────
assert abs(df.sum(axis=1) - 100).max() < 1e-6, "Las participaciones no suman 100%"


