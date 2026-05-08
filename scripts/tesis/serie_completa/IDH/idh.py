# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %%
# ═══════════════════════════════════════════════════════════════════
# GRÁFICA DE PERÍODOS ESTRUCTURALES — IDH
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
output_dir = ASSETS_DIR / "serie_completa" / "idh"
os.makedirs(output_dir, exist_ok=True)
set_style()

# ─────────────────────────── 2. CARGA DE DATOS ──────────────────────
with sqlite3.connect(str(DB_PATH)) as conn:
    df = (
        pd.read_sql(
            "SELECT año, total_idh FROM ingresos_nacionales WHERE año > 2004",
            conn,
            index_col="año",
        )
        .sort_index()
    )

# ──────────────── 3. COMPONENTES, COLORES Y ABREVIATURAS ────────────
componentes = [
    ("total_idh", "Total IDH"),
]
cols_componentes = [col for col, _ in componentes]

colors = {
    "total_idh": "#1f77b4",
}

abbr_map = {
    "total_idh": "IDH",
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
# Ajustar los valores (x_offset, y_offset) según la escala de la serie

hitos_offset_periodos = {year: 0.8 for year in hitos_v_periodos}

# Anotaciones de valores en años clave
annotation_offsets = {
    "total_idh": {
        1952: (0,  0),
        1985: (0,  0),
        2006: (-0.6, 200),
        2014: (0, 300),
        2022: (0, -320),
        2023: (0, -320),
    },
}

# Posición de medias por período  (año_centro, altura_relativa 0-1)
medias_offsets = {
    "Intervensionismo-estatal 52-84": (1960, 0.92),
    "Neoliberalismo 85-05":           (1990, 0.92),
    "E.S.C.P (I)":                    (2009, 0.92),
    "E.S.C.P (II)":                   (2019, 0.92),
}

# Posición de tasas de crecimiento  (año_centro, altura_relativa 0-1)
tasas_offsets = {
    "1952-1984": (1960, 0.83),
    "1985-2005": (1990, 0.83),
    "2006-2014": (2009, 0.83),
    "2015-2022": (2019, 0.83),
}

# ────────────────────────── 6. GRÁFICO BASE ─────────────────────────
fig, ax = init_base_plot(
    df=df,
    series=componentes,
    colors=colors,
    title=f"INGRESOS IDH ({df.index.min()}–{df.index.max()}) — Períodos Económicos",
    xlabel="Año",
    ylabel="Millones de bolivianos",
    source_text="Fuente: UDAPE",
)

# ──────────────────── 7. ELEMENTOS GRÁFICOS ─────────────────────────
add_hitos(ax, df.index, hitos_v_periodos, hitos_offset_periodos, line_kwargs={"lw": 0.9})

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

# ────────────────────────── 8. GUARDADO ─────────────────────────────
ax.set_ylim(-300, df['total_idh'].max() * 1.15)
plt.tight_layout()
fig.savefig(output_dir / "idh_periodos.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()

