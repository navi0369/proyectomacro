import nbformat

nb_path = "/home/navi/Desktop/proyectomacro-main/notebooks/tesis/serie_completa/grado_de_apertura.ipynb"

code = """# ═══════════════════════════════════════════════════════════════════
# GRÁFICA DE PERÍODOS ESTRUCTURALES — GRADO DE APERTURA
# ═══════════════════════════════════════════════════════════════════
import os
import sys
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from func_auxiliares.graficos_utils import (
    set_style,
    init_base_plot,
    add_hitos,
    add_cycle_means_multi,
    add_year_value_annotations,
    add_period_growth_annotations_multi,
    adjust_annot_years,
    adjust_cycles,
    adjust_periods,
    add_period_backgrounds,
)

from func_auxiliares.config import (
    DB_PATH,
    ASSETS_DIR,
    CYCLES_PERIODOS,
    annot_years_periodos,
    periodos_tasas_periodos,
    hitos_v_periodos,
)

# ─────────────────────── 1. CONFIGURACIÓN GENERAL ───────────────────
output_dir = ASSETS_DIR / "serie_completa" / "grado_de_apertura"
os.makedirs(output_dir, exist_ok=True)
set_style()

# ─────────────────────────── 2. CARGA DE DATOS ──────────────────────
with sqlite3.connect(str(DB_PATH)) as conn:
    df = (
        pd.read_sql(
            "SELECT * FROM grado_de_apertura",
            conn,
            index_col="año",
        )
        .sort_index()
    )

# ──────────────── 3. COMPONENTES, COLORES Y ABREVIATURAS ────────────
componentes = [
    ("grado", "Grado de Apertura (%)"),
]
cols_componentes = [col for col, _ in componentes]

colors = {
    "grado": "#f39c12",
}

abbr_map = {
    "grado": "G. Apertura",
}

# ──────────────── 4. PREPARACIÓN DE CICLOS Y PERÍODOS ───────────────
annotate_years = adjust_annot_years(df, annot_years_periodos)
cycles         = adjust_cycles(df, CYCLES_PERIODOS)
periods        = adjust_periods(df, periodos_tasas_periodos)

cycle_stats = {
    name: df.loc[period, cols_componentes].mean().to_dict()
    for name, period in cycles.items()
}

# ───────────────────── 5. OFFSETS DE POSICIONAMIENTO ────────────────
hitos_offset_periodos = {year: 0.8 for year in hitos_v_periodos}

annotation_offsets = {
    "grado": {
        1952: (0,  3),
        1985: (0,  3),
        2006: (0,  3),
        2014: (0, -6),
        2022: (0, -6),
    },
}

medias_offsets = {
    "INTERVENSIONISMO ESTATAL": (1960, 0.83),
    "NEOLIBERALISMO": (1998, 0.83),
    "E.S.C.P (I)":    (2006, 0.83),
    "E.S.C.P (II)":    (2015, 0.83),
}

tasas_offsets = {
    "1952-1984": (1960, 0.63),
    "1985-2005": (1998, 0.69),
    "2006-2014": (2006, 0.69),
    "2015-2024": (2015, 0.69),
}

# ────────────────────────── 6. GRÁFICO BASE ─────────────────────────
fig, ax = init_base_plot(
    df=df,
    series=componentes,
    colors=colors,
    title=f"Grado de Apertura de la Economía ({df.index.min()}–{df.index.max()}) — Períodos Económicos",
    xlabel="Año",
    ylabel="Porcentaje (%)",
    source_text="Fuente: Elaboración propia en base a datos del INE",
)

# ──────────────────── 7. ELEMENTOS GRÁFICOS ─────────────────────────
add_hitos(
    ax, 
    df.index, 
    hitos_v_periodos, 
    hitos_offset_periodos, 
    line_kwargs={"lw": 0.9})

add_cycle_means_multi(
    ax, cycle_stats, medias_offsets,
    abbr_map, colors,
    line_spacing=ax.get_ylim()[1] * 0.03,
)

add_year_value_annotations(
    ax, df, annotate_years,
    cols_componentes, annotation_offsets, colors,
    arrow_lw=0.5,
)

add_period_growth_annotations_multi(
    ax, df, periods,
    cols_componentes, tasas_offsets,
    colors, abbr_map,
)
add_period_backgrounds(
    ax,
    periods,
)

# ────────────────────────── 8. GUARDADO ─────────────────────────────
plt.tight_layout()
fig.savefig(output_dir / "grado_de_apertura_periodos.png", dpi=300, bbox_inches="tight")
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
