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
    df_plata = (pd.read_sql(
        "SELECT año, plata_volumen, plata_valor "
        "FROM exportaciones_minerales_totales WHERE año > 1991", conn)
        .set_index("año")
        .sort_index()
    )
    df_precio = (pd.read_sql(
        "SELECT año, plata AS precio_usd_ot "
        "FROM precio_oficial_minerales WHERE año > 1991", conn)
        .set_index("año")
        .sort_index()
    )

df = df_plata.join(df_precio, how="inner")
df["plata_valor_musd"] = df["plata_valor"] / 1_000   # miles → millones
df.drop(columns="plata_valor", inplace=True)

# ───────────────────────  GRÁFICA DUAL AXIS (valor-precio) ───────────────────────
cols   = ["plata_valor_musd", "precio_usd_ot"]
abbr   = {"plata_valor_musd": "Valor", "precio_usd_ot": "Precio"}
colors = {"plata_valor_musd": "#7f7f7f", "precio_usd_ot": "#1f77b4"}

cycle_stats = {n: df.loc[s, cols].mean().to_dict() for n, s in periods.items()}

hitos_v      = {2000: "Crisis", 2006: "Expansión", 2014: "Recesión"}
hitos_offset = {yr: .60 for yr in hitos_v}

anot_years = [1992, 2000, 2006, 2014, 2023]
annotation_offsets = {
    "plata_valor_musd": {
        1992:(0,25), 2000:(0,-45), 2006:(0,45),
        2014:(0.5,40), 2023:(0,30)
    },
    "precio_usd_ot": {
        1992:(0,-1), 2000:(0,0.6), 2006:(-0.5,1),
        2014:(-0.5,-1), 2023:(0.55,-1)
    },
}
growth_periods        = [(1992,2000),(2000,2006),(2006,2014),(2014,2023)]
period_growth_offsets = {
    "1992-2000": (1991,0.78), "2000-2006":(2001,0.78),
    "2006-2014": (2006.2,0.78), "2014-2023":(2016,0.78)
}
cycle_text_offsets = {
    "Expansión 92-99": (1991,0.92),
    "Crisis 00-05":    (2001,0.92),
    "Expansión 06-13": (2006.2,0.92),
    "Recesión 14-23":  (2016,0.92),
}

fig, ax_val = plt.subplots(figsize=(13,8))
ax_price    = ax_val.twinx()

ax_val.plot(df.index, df["plata_valor_musd"],
            label="Valor exportado (M USD)",
            color=colors["plata_valor_musd"])
ax_price.plot(df.index, df["precio_usd_ot"],
              label="Precio (USD/oz t)",
              color=colors["precio_usd_ot"])

add_hitos(ax_val, df.index, hitos_v, hitos_offset, line_kwargs={"lw":1})
add_cycle_means_multi(
    ax_val, cycle_stats, cycle_text_offsets,
    abbr, colors, line_spacing=df["plata_valor_musd"].max()*0.03,
    value_fmt="{:,.1f}"
)
add_year_value_annotations(
    ax_val, df, anot_years, ["plata_valor_musd"],
    {"plata_valor_musd": annotation_offsets["plata_valor_musd"]},
    {"plata_valor_musd": colors["plata_valor_musd"]}, arrow_lw=0.6
)
add_year_value_annotations(
    ax_price, df, anot_years, ["precio_usd_ot"],
    {"precio_usd_ot": annotation_offsets["precio_usd_ot"]},
    {"precio_usd_ot": colors["precio_usd_ot"]}, arrow_lw=0.6,
    value_fmt="{:,.1f}"
)
add_period_growth_annotations_multi(
    ax_val, df, growth_periods, cols,
    period_growth_offsets, colors, abbr
)

ax_val.set_title(f"Plata: Valor vs. Precio ({df.index[0]}–{df.index[-1]})",
                 fontweight="bold")
ax_val.set_xlabel("Año")
ax_val.set_ylabel("Valor exportado (millones USD)",
                  color=colors["plata_valor_musd"])
ax_price.set_ylabel("Precio (USD por onza t)",
                    color=colors["precio_usd_ot"])
ax_val.tick_params(axis="y", labelcolor=colors["plata_valor_musd"])
ax_price.tick_params(axis="y", labelcolor=colors["precio_usd_ot"])
ax_val.set_xticks(df.index[::max(1,len(df)//31)])
ax_val.tick_params(axis="x", rotation=45)

h,l   = ax_val.get_legend_handles_labels()
h2,l2 = ax_price.get_legend_handles_labels()
hl    = [(x,y) for x,y in zip(h+h2, l+l2) if not y.startswith('_')]
if hl: ax_val.legend(*zip(*hl), loc="upper left", fontsize=11)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "plata_valor_precio_dual_axis.png"), dpi=300)
plt.show()

# ──────────────────  GRÁFICA DUAL AXIS (volumen-precio) ──────────────────
cols_vol   = ["plata_volumen", "precio_usd_ot"]
colors_vol = {
    "plata_volumen": "tab:gray",
    "precio_usd_ot": colors["precio_usd_ot"]          # azul del gráfico principal
}
abbr_vol = {"plata_volumen": "Vol", "precio_usd_ot": "P"}

cycle_stats_vol = {
    n: df.loc[s, cols_vol].mean().to_dict()
    for n, s in periods.items()
}

annotation_offsets_vol = {
    "plata_volumen": {
        1992:(0,40), 2000:(0,20), 2006:(0.5,-25),
        2014:(0,20), 2023:(0,15)
    },
    "precio_usd_ot": {
        1992:(0,-1), 2000:(0,-0.73), 2006:(-0.1,1.2),
        2014:(-1,-1), 2023:(0.55,-1)
    }
}

period_growth_offsets_vol = {
    "1992-2000": (1995,0.80), "2000-2006":(2002,0.80),
    "2006-2014": (2008,0.33), "2014-2023":(2016,0.33)
}

cycle_text_offsets_vol = {
    "Expansión 92-99": (1995,0.90),
    "Crisis 00-05":    (2002,0.90),
    "Expansión 06-13": (2008,0.43),
    "Recesión 14-23":  (2016,0.43),
}

fig_v, ax_v = plt.subplots(figsize=(13,8))
ax_price_v = ax_v.twinx()

# series
ax_v.plot(df.index, df["plata_volumen"],
          label="Volumen (kg finos)",
          color=colors_vol["plata_volumen"])
ax_price_v.plot(df.index, df["precio_usd_ot"],
                label="Precio (USD/oz t)",
                color=colors_vol["precio_usd_ot"])

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
    ax_v, df, anot_years, ["plata_volumen"],
    {"plata_volumen": annotation_offsets_vol["plata_volumen"]},
    {"plata_volumen": colors_vol["plata_volumen"]}, arrow_lw=0.6
)
add_year_value_annotations(
    ax_price_v, df, anot_years, ["precio_usd_ot"],
    {"precio_usd_ot": annotation_offsets_vol["precio_usd_ot"]},
    {"precio_usd_ot": colors_vol["precio_usd_ot"]}, arrow_lw=0.6,
    value_fmt="{:,.1f}"
)

# tasas de crecimiento
add_period_growth_annotations_multi(
    ax_v, df, growth_periods, cols_vol,
    period_growth_offsets_vol, colors_vol, abbr_vol,
    line_spacing_ratio=0.03
)

# ejes y leyenda
ax_v.set_title(f"Plata: Volumen vs. Precio ({df.index[0]}–{df.index[-1]})",
               fontweight="bold")
ax_v.set_xlabel("Año")
ax_v.set_ylabel("Volumen (kg finos)", color=colors_vol["plata_volumen"])
ax_price_v.set_ylabel("Precio (USD por onza t)", color=colors_vol["precio_usd_ot"])
ax_v.tick_params(axis="y", labelcolor=colors_vol["plata_volumen"])
ax_price_v.tick_params(axis="y", labelcolor=colors_vol["precio_usd_ot"])
ax_v.set_xticks(df.index[::max(1,len(df)//31)])
ax_v.tick_params(axis="x", rotation=45)

h1,l1 = ax_v.get_legend_handles_labels()
h2,l2 = ax_price_v.get_legend_handles_labels()
ax_v.legend(h1+h2, l1+l2, loc="upper left", fontsize=11)

plt.tight_layout()
plt.savefig(os.path.join(output_dir,"plata_volumen_precio_dual_axis.png"), dpi=300)
plt.show()


