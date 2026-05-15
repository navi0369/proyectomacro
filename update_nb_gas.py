import nbformat

nb_path = "/home/navi/Desktop/proyectomacro-main/notebooks/tesis/serie_completa/exportaciones/participacion_gas_natural_y_otros_hidrocarburos.ipynb"

code = """# ═══════════════════════════════════════════════════════════════════
# GRÁFICA DE PERÍODOS ESTRUCTURALES (BARRAS) — PARTICIPACIÓN DE GAS Y OTROS HIDROCARBUROS
# ═══════════════════════════════════════════════════════════════════
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from func_auxiliares.graficos_utils import (
    set_style,
    plot_stacked_bar,
    add_hitos_barras,
    add_cycle_means_barras,
    adjust_cycles,
)

from func_auxiliares.config import (
    DB_PATH,
    ASSETS_DIR,
    CYCLES_PERIODOS,
    hitos_v_periodos,
)

# ─────────────────────── 1. CONFIGURACIÓN GENERAL ───────────────────
OUTPUT_DIR = ASSETS_DIR / "serie_completa" / "exportaciones" / "participacion_gas_natural_y_otros_hidrocarburos"
os.makedirs(OUTPUT_DIR, exist_ok=True)
set_style()

# ─────────────────────────── 2. CARGA DE DATOS ──────────────────────
with sqlite3.connect(str(DB_PATH)) as conn:
    df = pd.read_sql("SELECT año, exportacion_gas, otros_hidrocarburos FROM participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos", conn, index_col="año")

cycles_adj = adjust_cycles(df, CYCLES_PERIODOS)

# Para la gráfica base usaremos data_plot como el DataFrame final.
data_plot = df 

# ──────────────── 3. COMPONENTES Y ESTADÍSTICAS ────────────
componentes = [
    ("exportacion_gas", "Gas Natural"),
    ("otros_hidrocarburos", "Otros Hidrocarburos"),
]
cols = [c for c, _ in componentes]

# Cálculo de estadísticas promedio por ciclo
cycle_stats = {
    name: data_plot.loc[sl, cols].mean().to_dict()
    for name, sl in cycles_adj.items()
}

# ───────────────────── 4. OFFSETS DE POSICIONAMIENTO ────────────────
hitos_offset = {}
hitos_text_x = {}

# Offsets manuales para mover las anotaciones de la media de alguna columna
MEAN_OFFSETS_BY_NAME = {}

# Componentes de las que NO se quiere mostrar el promedio en el gráfico
SKIP_MEANS_BY_NAME = {}

# ────────────────────────── 5. PLOT Y ANOTACIONES ─────────────────────────
fig, ax = plot_stacked_bar(
    data_plot, 
    series=componentes,
    title="Participación de Gas Natural y Otros Hidrocarburos en el\\nTotal de Exportaciones de Hidrocarburos (%)\\n",
    legend_ncol=2
)

add_hitos_barras(
    ax, data_plot.index, hitos_v_periodos, hitos_offset, hitos_text_x
)

add_cycle_means_barras(
    ax,
    index=list(data_plot.index),   # secuencia de años
    cycle_slices=cycles_adj,       # nombre → slice
    cycle_stats=cycle_stats,       # nombre → {col: media}
    cols=cols,                     # orden de apilado
    offsets=MEAN_OFFSETS_BY_NAME,  # opcional
    skip=SKIP_MEANS_BY_NAME        # opcional
)

# ────────────────────────── 6. GUARDADO ─────────────────────────────
plt.tight_layout()
out_path = OUTPUT_DIR / "participacion_gas_natural_y_otros_hidrocarburos_periodos.png"
plt.savefig(out_path, dpi=300, bbox_inches="tight")
plt.show()
plt.close()
"""

with open(nb_path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

new_cell = nbformat.v4.new_code_cell(source=code)
nb.cells = [new_cell]

with open(nb_path, "w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print("Notebook updated successfully.")
