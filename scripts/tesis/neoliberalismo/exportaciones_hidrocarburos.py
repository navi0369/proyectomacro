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

# ── Parámetros generales ──────────────────────────────────────────────────────
OUTPUT_DIR = "../../../assets/tesis/neoliberalismo/serie_completa"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CRISIS_YEARS = slice(1982, 1986)   # 1982-1985 inclusive
POST_YEARS   = slice(1986, 2002)   # 1986-2002 inclusive

# ── Estilo profesional ────────────────────────────────────────────────────────
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "font.family": "serif", "font.size": 12,
    "axes.titlesize": 16, "axes.labelsize": 14,
    "grid.linestyle": "--", "lines.linewidth": 2,
    "figure.dpi": 150, "savefig.bbox": "tight"
})

# ── Conexión y carga de datos ─────────────────────────────────────────────────
with sqlite3.connect("../../../db/proyectomacro.db") as conn:
    df = pd.read_sql_query(
        "SELECT * FROM participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos",
        conn
    )

df.set_index("año", inplace=True)
df = df.loc[1982:2002]   # periodo 1982-2002

# ── Estadísticas promedio por periodo ────────────────────────────────────────
avg_crisis = df.loc[CRISIS_YEARS].mean()
avg_post   = df.loc[POST_YEARS].mean()

# ── Gráfico stacked-bar por año ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(15, 7))
df.plot(kind="bar", stacked=True, ax=ax, width=0.8)

ax.set_ylabel("Participación (%)")
ax.set_xlabel("Año")
ax.set_title(
    "Participación de Gas y Otros Hidrocarburos (1982-2002)",
    fontweight="bold"
)
ax.legend(["Gas Natural", "Otros Hidrocarburos"], loc="upper left",
          bbox_to_anchor=(1, 1))
plt.xticks(rotation=45)

# ── Cajas de resumen ──────────────────────────────────────────────────────────
stats_crisis = (
    f"Gas Natural:       {avg_crisis['exportacion_gas']:.1f}%\n"
    f"Otros hidrocarburos: {avg_crisis['otros_hidrocarburos']:.1f}%"
)
stats_post = (
    f"Gas Natural:       {avg_post['exportacion_gas']:.1f}%\n"
    f"Otros hidrocarburos: {avg_post['otros_hidrocarburos']:.1f}%"
)

ax.text(1.02, 0.65, "Crisis (82-85)\n" + stats_crisis,
        transform=ax.transAxes, fontsize=10, va="center", ha="left",
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="black"))
ax.text(1.02, 0.30, "Post-crisis (86-02)\n" + stats_post,
        transform=ax.transAxes, fontsize=10, va="center", ha="left",
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="black"))

# ── Guardar y mostrar ────────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "participacion_gas_hidrocarburos_82_02.png"),
            dpi=300)
plt.show()

