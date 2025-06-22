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
# ─────────────────────────────────────────────────────────────
# Importaciones comunes
# ─────────────────────────────────────────────────────────────
import sys, os, sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath('../'))  # utilidades propias
from graficos_utils import *
from config import (
    # Con‑crisis
    CYCLES, annot_years, periodos_tasas, hitos_v,
    # Sin‑crisis
    CYCLES_SIN_CRISIS, annot_years_sin_crisis,
    periodos_tasas_sin_crisis, hitos_v_sin_crisis,
    # Periodos estructurales
    CYCLES_PERIODOS, annot_years_periodos,
    periodos_tasas_periodos, hitos_v_periodos,
)

# Directorio de salida y estilo global
output_dir = "../../../../assets/tesis/serie_completa/deuda_interna"
os.makedirs(output_dir, exist_ok=True)
set_style()

# ─────────────────────────────────────────────────────────────
# Carga de datos
# ─────────────────────────────────────────────────────────────
with sqlite3.connect('../../../../db/proyectomacro.db') as conn:
    df_di = (
        pd.read_sql('SELECT * FROM deuda_interna', conn)
          .set_index('año')
          .sort_index()
    )

# ─────────────────────────────────────────────────────────────
# Componentes comunes
# ─────────────────────────────────────────────────────────────
componentes = [('valor', 'Deuda interna total')]
cols_componentes = ['valor']
abbr_map = {'valor': 'Deuda int.'}
custom_colors = {'valor': '#d62728'}


# ============================================================
# 1) PRIMERA GRÁFICA — CON CRISIS
# ============================================================
# Preparación
annotate_years       = adjust_annot_years(df_di, annot_years)
cycles_stats         = {n: df_di.loc[s, cols_componentes].mean().to_dict()
                        for n, s in adjust_cycles(df_di, CYCLES).items()}
periodos             = adjust_periods(df_di, periodos_tasas)

# Offsets
annotation_offsets = {
    'valor': {
        1992: (0, 150), 2000: (0, 150), 2006: (0, 150),
        2014: (0.5, 150), 2024: (1, 150),
    }
}
hitos_offset         = {a: 0.8 for a in hitos_v}
medias_offsets       = {
    'Expansión 93-99': (1993, 1),
    'Crisis 00-05':    (2000, 1),
    'Expansión 06-13': (2006, 1),
    'Recesión 14-22':  (2014, 1),
}
tasas_offsets        = {
    '1993-2000': (1993, 0.83),
    '2000-2006': (2003, 0.83),
    '2006-2014': (2010, 0.83),
    '2014-2022': (2018, 0.65),
}

# Gráfica
fig, ax = init_base_plot(
    df_di, componentes, custom_colors,
    "Deuda Interna TGÑ (1993–2022) — Ciclos con Crisis",
    "Año", "Millones de dólares",
    source_text="Fuente: UDAPE"
)
add_hitos(ax, df_di.index, hitos_v, hitos_offset, line_kwargs={'lw': 0.9})
add_cycle_means_multi(ax, cycles_stats, medias_offsets, abbr_map, custom_colors,
                      line_spacing=ax.get_ylim()[1]*0.03)
add_year_value_annotations(ax, df_di, annotate_years, cols_componentes,
                           annotation_offsets, custom_colors, arrow_lw=0.5)
add_period_growth_annotations_multi(ax, df_di, periodos, cols_componentes,
                                    tasas_offsets, custom_colors, abbr_map)

ax.set_ylim(-300, df_di['valor'].max()*1.15)
plt.savefig(os.path.join(output_dir, "deuda_interna_ciclos.png"))
plt.show()
plt.close()


# %%
# ============================================================
# 2) SEGUNDA GRÁFICA — SIN CRISIS
# ============================================================
# Preparación
annotate_years_sin_crisis = adjust_annot_years(df_di, annot_years_sin_crisis)
cycles_stats_sin_crisis   = {n: df_di.loc[s, cols_componentes].mean().to_dict()
                             for n, s in adjust_cycles(df_di, CYCLES_SIN_CRISIS).items()}
periodos_sin_crisis       = adjust_periods(df_di, periodos_tasas_sin_crisis)

# Offsets
annotation_offsets_sin_crisis = {
    'valor': {
        1993: (0, 500), 2005: (0, 500), 2015: (0, 500), 2022: (0, 500)
    }
}
hitos_offset_sin_crisis       = {a: 0.8 for a in hitos_v_sin_crisis}
medias_offsets_sin_crisis     = {
    'Expansión 93-05': (1993, 1),
    'Expansión 06-14': (2006, 1),
    'Recesión 15-22':  (2014, 1),
}
tasas_offsets_sin_crisis = {
    '1993-2005': (1993, 1.05),
    '2006-2014': (2006, 1.05),
    '2015-2022': (2015, 1.05)
}

# Gráfica
fig, ax = init_base_plot(
    df_di, componentes, custom_colors,
    "Deuda Interna TGÑ (1993–2022) — Sin Crisis",
    "Año", "Millones de dólares",
    source_text="Fuente: UDAPE"
)
add_hitos(ax, df_di.index, hitos_v_sin_crisis, hitos_offset_sin_crisis, line_kwargs={'lw':0.9})
add_cycle_means_multi(ax, cycles_stats_sin_crisis, medias_offsets_sin_crisis,
                      abbr_map, custom_colors, line_spacing=ax.get_ylim()[1]*0.03)
add_year_value_annotations(ax, df_di, annotate_years_sin_crisis, cols_componentes,
                           annotation_offsets_sin_crisis, custom_colors, arrow_lw=0.5)
add_period_growth_annotations_multi(ax, df_di, periodos_sin_crisis, cols_componentes,
                                    tasas_offsets_sin_crisis, custom_colors, abbr_map)

ax.set_ylim(-300, df_di['valor'].max()*1.15)
plt.savefig(os.path.join(output_dir, "deuda_interna_sin_crisis.png"))
plt.show()
plt.close()

# %%
# ============================================================
# 3) TERCERA GRÁFICA — PERIODOS ESTRUCTURALES
# ============================================================
# Preparación
annotate_years_periodos = adjust_annot_years(df_di, annot_years_periodos)
cycles_stats_periodos   = {n: df_di.loc[s, cols_componentes].mean().to_dict()
                           for n, s in adjust_cycles(df_di, CYCLES_PERIODOS).items()}
periodos_periodos       = adjust_periods(df_di, periodos_tasas_periodos)

# Offsets
annotation_offsets_periodos = {
    'valor': {
        1993: (-1.5, 1),
        2006: (0, 1),
        2022: (0, 1),
    }
}
hitos_offset_periodos       = {a: 0.8 for a in hitos_v_periodos}
medias_offsets_periodos     = {
    'Neoliberalismo 93-05':    (1993, 1),
    'Neodesarrollismo 06-22':  (2006, 1),
}
# Tasas y participación específicas del resumen

tasas_offsets_periodos = {
    '1993-2005': (1995, 0.83),
    '2006-2022': (2014, 0.65),
}
# Gráfica
fig, ax = init_base_plot(
    df_di, componentes, custom_colors,
    "Deuda Interna TGÑ (1993–2022) — Periodos Económicos",
    "Año", "Millones de dólares",
    source_text="Fuente: UDAPE"
)
add_hitos(ax, df_di.index, hitos_v_periodos, hitos_offset_periodos,
          annotate_labels=tuple(), line_kwargs={'lw':1.0})
add_cycle_means_multi(ax, cycles_stats_periodos, medias_offsets_periodos,
                      abbr_map, custom_colors, line_spacing=ax.get_ylim()[1]*0.03)
add_year_value_annotations(ax, df_di, annotate_years_periodos, cols_componentes,
                           annotation_offsets_periodos, custom_colors, arrow_lw=0.5)
add_period_growth_annotations_multi(ax, df_di, periodos_periodos, cols_componentes,
                                    tasas_offsets_periodos, custom_colors, abbr_map)
plt.savefig(os.path.join(output_dir, "deuda_interna_periodos.png"))
plt.show()
plt.close()

