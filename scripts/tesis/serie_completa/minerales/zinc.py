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
# ─────────────────────────────  PREPARACIÓN  ──────────────────────────────
import sys, os, sqlite3
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath('../'))
from graficos_utils import (
    add_hitos, add_cycle_means_multi,
    add_year_value_annotations, add_period_growth_annotations_multi
)

# 0. Ciclos y carpetas
periods = {
    "Expansión 92-99": slice(1992, 1999),
    "Crisis 00-05":    slice(2000, 2005),
    "Expansión 06-13": slice(2006, 2013),
    "Recesión 14-23":  slice(2014, 2023),
}
output_dir = "../../../../assets/tesis/serie_completa/minerales"
os.makedirs(output_dir, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update({
    "font.family": "serif", "font.size": 12,
    "axes.titlesize": 16,   "axes.labelsize": 14,
    "grid.linestyle": "--", "lines.linewidth": 2,
    "figure.dpi": 150,      "savefig.bbox": "tight",
})

# 1. Datos ────────────────────────────────────────────────────────────────
with sqlite3.connect("../../../../db/proyectomacro.db") as conn:
    df_zinc = (pd.read_sql(
        "SELECT año, zinc_volumen, zinc_valor FROM exportaciones_minerales_totales "
        "WHERE año > 1991", conn)
        .set_index("año")
        .sort_index()
    )
    df_precio = (pd.read_sql(
        "SELECT año, zinc AS precio_usd_oz "
        "FROM precio_oficial_minerales WHERE año > 1991", conn)
        .set_index("año")
        .sort_index()
    )

df = df_zinc.join(df_precio, how="inner")
df["zinc_valor_musd"] = df["zinc_valor"] / 1_000     # miles → millones
df.drop(columns="zinc_valor", inplace=True)

# ───────────────────────  GRÁFICA DUAL AXIS (valor-precio) ───────────────────────
cols     = ["zinc_valor_musd", "precio_usd_oz"]
abbr     = {"zinc_valor_musd": "Valor", "precio_usd_oz": "Precio"}
colors   = {"zinc_valor_musd": "#1f77b4", "precio_usd_oz": "#d62728"}

cols_dual = ["zinc_valor_musd", "precio_usd_oz"]

cycle_stats = {
    nombre: df.loc[rango, cols_dual].mean().to_dict()
    for nombre, rango in periods.items()
}
print(cycle_stats)
hitos_v       = {2000: "Crisis", 2006: "Expansión", 2014: "Recesión"}
hitos_offset  = {yr: .60 for yr in hitos_v}

anot_years = [1992, 2000, 2006, 2014, 2023]
annotation_offsets = {
    "zinc_valor_musd": {
        1992:(0,50), 2000:(0,-80), 2006:(0,90), 2014:(0,60), 2023:(0,-50)
    },
    "precio_usd_oz": {
        1992:(0,-0.03),  2000:(0.13,0.08),  2006:(0,0.05), 2014:(0,-0.1), 2023:(0.5,-0.03)
    },
}
growth_periods        = [(1992,2000),(2000,2006),(2006,2014),(2014,2023)]
period_growth_offsets = {
    "1992-2000": (1991,0.76), "2000-2006":(2001,0.76),
    "2006-2014": (2008,0.76), "2014-2023":(2016,0.26)
}
cycle_text_offsets = {
    "Expansión 92-99": (1991,0.9),
    "Crisis 00-05":    (2001,0.9),
    "Expansión 06-13": (2008,0.9),
    "Recesión 14-23":  (2016,0.4),
}

fig, ax_val = plt.subplots(figsize=(13,8))
ax_price    = ax_val.twinx()

# series
ax_val.plot(df.index, df["zinc_valor_musd"], label="Valor exportado (M USD)",
            color=colors["zinc_valor_musd"])
ax_price.plot(df.index, df["precio_usd_oz"],   label="Precio (USD/oz)",
            color=colors["precio_usd_oz"])

# helpers
add_hitos(ax_val, df.index, hitos_v, hitos_offset, line_kwargs={"linewidth":1})
add_cycle_means_multi(ax_val, cycle_stats, cycle_text_offsets,
                      abbr, colors, line_spacing=df["zinc_valor_musd"].max()*0.03,
                      value_fmt="{:,.1f}")
add_year_value_annotations(
    ax_val,   df, anot_years, ["zinc_valor_musd"],
    {"zinc_valor_musd": annotation_offsets["zinc_valor_musd"]},
    {"zinc_valor_musd": colors["zinc_valor_musd"]}, arrow_lw=0.6
)
add_year_value_annotations(
    ax_price, df, anot_years, ["precio_usd_oz"],
    {"precio_usd_oz": annotation_offsets["precio_usd_oz"]},
    {"precio_usd_oz": colors["precio_usd_oz"]}, arrow_lw=0.6,
    value_fmt="{:,.1f}"
)
add_period_growth_annotations_multi(
    ax_val, df, growth_periods, cols,
    period_growth_offsets, colors, abbr
)

# etiquetas
ax_val.set_title(f"Zinc: Valor vs. Precio ({df.index[0]}–{df.index[-1]})",
                 fontweight="bold")
ax_val.set_xlabel("Año")
ax_val.set_ylabel("Valor exportado (millones USD)", color=colors["zinc_valor_musd"])
ax_price.set_ylabel("Precio (USD por onza)",         color=colors["precio_usd_oz"])
ax_val.tick_params(axis="y", labelcolor=colors["zinc_valor_musd"])
ax_price.tick_params(axis="y", labelcolor=colors["precio_usd_oz"])
ax_val.set_xticks(df.index[::max(1,len(df)//31)])
ax_val.tick_params(axis="x", rotation=45)

# leyenda filtrada
h,l = ax_val.get_legend_handles_labels()
h2,l2 = ax_price.get_legend_handles_labels()
hl = [(x,y) for x,y in zip(h+h2,l+l2) if not y.startswith('_')]
if hl: ax_val.legend(*zip(*hl), loc="upper left", fontsize=11)

plt.tight_layout()
plt.savefig(os.path.join(output_dir,"zinc_valor_precio_dual_axis.png"), dpi=300)
plt.show()

# ──────────────────  GRÁFICA DUAL AXIS (volumen-precio) ──────────────────
cols_vol   = ["zinc_volumen", "precio_usd_oz"]
colors_vol = {
    "zinc_volumen": "tab:blue",
    "precio_usd_oz": colors["precio_usd_oz"]       # rojo definido antes
}
abbr_vol = {"zinc_volumen": "Vol", "precio_usd_oz": "P"}

cycle_stats_vol = {
    n: df.loc[s, cols_vol].mean().to_dict()
    for n, s in periods.items()
}

annotation_offsets_vol = {
    "zinc_volumen": {
        1992:(0,1e4), 2000:(-0.5,-2.2e4), 2006:(0,-3.7e4),
        2014:(0,1e4), 2023:(0,2.8e4)
    },
    "precio_usd_oz": {
        1992:(0,-0.03), 2000:(0.13,0.08), 2006:(0,0.05),
        2014:(0,-0.1),  2023:(0.5,-0.03)
    }
}

period_growth_offsets_vol = {
    "1992-2000": (1991,0.84), "2000-2006":(2000.2,0.84),
    "2006-2014": (2008,0.91), "2014-2023":(2016,0.39)
}

cycle_text_offsets_vol = {
    "Expansión 92-99": (1991,0.93),
    "Crisis 00-05":    (2000.2,0.93),
    "Expansión 06-13": (2008,0.99),
    "Recesión 14-23":  (2016,0.50),
}

fig_v, ax_v = plt.subplots(figsize=(13,8))
ax_price_v  = ax_v.twinx()

# series
ax_v.plot(df.index, df["zinc_volumen"],
          label="Volumen (kg finos)",
          color=colors_vol["zinc_volumen"])
ax_price_v.plot(df.index, df["precio_usd_oz"],
                label="Precio (USD/oz)",
                color=colors_vol["precio_usd_oz"])

# hitos
add_hitos(ax_v, df.index, hitos_v, hitos_offset, line_kwargs={"lw":1})

# espaciado relativo
y_min, y_max = ax_v.get_ylim()
line_spacing = (y_max - y_min) * 0.03

# medias por ciclo
add_cycle_means_multi(
    ax_v, cycle_stats_vol, cycle_text_offsets_vol,
    abbr_vol, colors_vol, line_spacing=line_spacing,
    value_fmt="{:,.1f}"
)

# anotaciones de año
add_year_value_annotations(
    ax_v, df, anot_years, ["zinc_volumen"],
    {"zinc_volumen": annotation_offsets_vol["zinc_volumen"]},
    {"zinc_volumen": colors_vol["zinc_volumen"]}, arrow_lw=0.6
)
add_year_value_annotations(
    ax_price_v, df, anot_years, ["precio_usd_oz"],
    {"precio_usd_oz": annotation_offsets_vol["precio_usd_oz"]},
    {"precio_usd_oz": colors_vol["precio_usd_oz"]}, arrow_lw=0.6,
    value_fmt="{:,.1f}"
)

# tasas de crecimiento
add_period_growth_annotations_multi(
    ax_v, df, growth_periods, cols_vol,
    period_growth_offsets_vol, colors_vol, abbr_vol,
    line_spacing_ratio=0.03
)

# ejes y leyenda
ax_v.set_title(f"Zinc: Volumen vs. Precio ({df.index[0]}–{df.index[-1]})",
               fontweight="bold")
ax_v.set_xlabel("Año")
ax_v.set_ylabel("Volumen (kg finos)", color=colors_vol["zinc_volumen"])
ax_price_v.set_ylabel("Precio (USD por onza)", color=colors_vol["precio_usd_oz"])
ax_v.tick_params(axis="y", labelcolor=colors_vol["zinc_volumen"])
ax_price_v.tick_params(axis="y", labelcolor=colors_vol["precio_usd_oz"])
ax_v.set_xticks(df.index[::max(1,len(df)//31)])
ax_v.tick_params(axis="x", rotation=45)

h1,l1 = ax_v.get_legend_handles_labels()
h2,l2 = ax_price_v.get_legend_handles_labels()
ax_v.legend(h1+h2, l1+l2, loc="upper left", fontsize=11)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "zinc_volumen_precio_dual_axis.png"), dpi=300)
plt.show()

