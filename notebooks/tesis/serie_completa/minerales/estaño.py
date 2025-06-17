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
# ─────────────────────────────  PREPARACIÓN  ──────────────────────────────
import sys, os, sqlite3
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath('../'))
from graficos_utils import *
from config import *

# 0. Ciclos y carpetas
output_dir = "../../../../assets/tesis/serie_completa/minerales"
os.makedirs(output_dir, exist_ok=True)
set_style()

# 1. Datos ────────────────────────────────────────────────────────────────
df_estanio = get_df(
    sql="SELECT año, estaño_volumen, estaño_valor "
        "FROM exportaciones_minerales_totales WHERE año > 1991",
    conn_str="../../../../db/proyectomacro.db",
)
df_precio = get_df(
    sql="SELECT año, estaño AS precio_usd_lf "
        "FROM precio_oficial_minerales WHERE año > 1991",
    conn_str="../../../../db/proyectomacro.db",
)

df = df_estanio.join(df_precio, how="inner")
df["estanio_valor_musd"] = df["estaño_valor"] / 1_000        # miles → millones
df.drop(columns="estaño_valor", inplace=True)

# ───────────────────────  GRÁFICA DUAL AXIS (valor-precio) ───────────────────────
cols   = ["estanio_valor_musd", "precio_usd_lf"]
abbr   = {"estanio_valor_musd": "Valor", "precio_usd_lf": "Precio"}
colors = {"estanio_valor_musd": "#4682b4", "precio_usd_lf": "#d62728"}  # azul acero + rojo

CYCLES=adjust_cycles(df,CYCLES)
cycle_stats = {n: df.loc[s, cols].mean().to_dict() for n, s in CYCLES.items()}
hitos_offset = {yr: .60 for yr in hitos_v}

anot_years = [1992, 2000, 2006, 2014, 2023]
annotation_offsets = {                     # ↙ ajusta tras ver la figura
    "estanio_valor_musd": {
        1992:(0,5), 2000:(0,-15), 2006:(0,-25),
        2014:(-0.5,-25), 2023:(0,-10)
    },
    "precio_usd_lf": {
        1992:(0,-0.3), 2000:(0.13,0.3), 2006:(-0.4,0.6),
        2014:(0.5,0.3), 2023:(0.4,-2)
    },
}
growth_periods        = [(1992,2000),(2000,2006),(2006,2014),(2014,2023)]
period_growth_offsets = {
    "1992-2000": (1991,0.78), "2000-2006":(2001,0.78),
    "2006-2014": (2008,0.89), "2014-2023":(2016,0.89)
}
cycle_text_offsets = {
    "Expansión 92-99": (1991,0.92),
    "Crisis 00-05":    (2001,0.92),
    "Expansión 06-13": (2008,0.98),
    "Recesión 14-23":  (2016,0.98),
}

fig, ax_val = plt.subplots(figsize=(13,8))
ax_price    = ax_val.twinx()

ax_val.plot(df.index, df["estanio_valor_musd"],
            label="Valor exportado (M USD)",
            color=colors["estanio_valor_musd"])
ax_price.plot(df.index, df["precio_usd_lf"],
              label="Precio (USD/libra fina)",
              color=colors["precio_usd_lf"])

add_hitos(ax_val, df.index, hitos_v, hitos_offset, line_kwargs={"lw":1})
add_cycle_means_multi(
    ax_val, cycle_stats, cycle_text_offsets,
    abbr, colors,
    line_spacing=df["estanio_valor_musd"].max()*0.03,
    value_fmt="{:,.1f}"
)
add_year_value_annotations(
    ax_val, df, anot_years, ["estanio_valor_musd"],
    {"estanio_valor_musd": annotation_offsets["estanio_valor_musd"]},
    {"estanio_valor_musd": colors["estanio_valor_musd"]},
    arrow_lw=0.6
)
add_year_value_annotations(
    ax_price, df, anot_years, ["precio_usd_lf"],
    {"precio_usd_lf": annotation_offsets["precio_usd_lf"]},
    {"precio_usd_lf": colors["precio_usd_lf"]},
    arrow_lw=0.6,
    value_fmt="{:,.1f}"
)
add_period_growth_annotations_multi(
    ax_val, df, growth_periods, cols,
    period_growth_offsets, colors, abbr
)

ax_val.set_title(f"Estaño: Valor vs. Precio ({df.index[0]}–{df.index[-1]})",
                 fontweight="bold")
ax_val.set_xlabel("Año")
ax_val.set_ylabel("Valor exportado (millones USD)",
                  color=colors["estanio_valor_musd"])
ax_price.set_ylabel("Precio (USD por libra fina)",
                    color=colors["precio_usd_lf"])
ax_val.tick_params(axis="y", labelcolor=colors["estanio_valor_musd"])
ax_val.tick_params(axis="x", rotation=45)

h,l   = ax_val.get_legend_handles_labels()
h2,l2 = ax_price.get_legend_handles_labels()
hl    = [(x,y) for x,y in zip(h+h2, l+l2) if not y.startswith('_')]
if hl: ax_val.legend(*zip(*hl), loc="upper left", fontsize=11)

ax_val.set_xticks(df.index[::max(1, len(df)//31)])

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "estanio_valor_precio_dual_axis.png"), dpi=300)
plt.show()

# ──────────────────  GRÁFICA DUAL AXIS (volumen-precio) ──────────────────
cols_vol   = ["estaño_volumen", "precio_usd_lf"]
colors_vol = {
    "estaño_volumen": "tab:blue",
    "precio_usd_lf":  colors["precio_usd_lf"]   # rojo que definiste arriba
}
abbr_vol = {"estaño_volumen": "Vol", "precio_usd_lf": "P"}

cycle_stats_vol = {
    n: df.loc[s, cols_vol].mean().to_dict()
    for n, s in CYCLES.items()
}
hitos_offset_v = {yr: .81 for yr in hitos_v}
annotation_offsets_vol = {
    "estaño_volumen": {
        1992:(-0.6,-600), 2000:(0,100), 2006:(0,100),
        2014:(0,120), 2023:(0,-350)
    },
    "precio_usd_lf": {
        1992:(0,-0.3), 2000:(0.15,0.4), 2006:(-0.4,0.6),
        2014:(0.4,0.4), 2023:(0.4,-0.5)
    }
}

period_growth_offsets_vol = {
    "1992-2000": (1995,0.90), "2000-2006":(2001,0.96),
    "2006-2014": (2006.2,0.96), "2014-2023":(2016,0.96)
}

cycle_text_offsets_vol = {
    "Expansión 92-99": (1995,0.95),
    "Crisis 00-05":    (2001,1.00),
    "Expansión 06-13": (2006.2,1.00),
    "Recesión 14-23":  (2016,1.00),
}

fig_v, ax_v = plt.subplots(figsize=(13,8))
ax_price = ax_v.twinx()

# series
ax_v.plot(df.index, df["estaño_volumen"],
          label="Volumen (kg finos)",
          color=colors_vol["estaño_volumen"])
ax_price.plot(df.index, df["precio_usd_lf"],
              label="Precio (USD/libra fina)",
              color=colors_vol["precio_usd_lf"])

# hitos ciclo
add_hitos(ax_v, df.index, hitos_v, hitos_offset_v, line_kwargs={"lw":1})
print(hitos_v)
# espaciado 3 % del rango visible
y_min, y_max = ax_v.get_ylim()
line_spacing = (y_max - y_min) * 0.03

# medias por ciclo
add_cycle_means_multi(
    ax_v, cycle_stats_vol, cycle_text_offsets_vol,
    abbr_vol, colors_vol, line_spacing=line_spacing,
    value_fmt="{:,.1f}"
)

# anotaciones de valores
add_year_value_annotations(
    ax_v, df, anot_years, ["estaño_volumen"],
    {"estaño_volumen": annotation_offsets_vol["estaño_volumen"]},
    {"estaño_volumen": colors_vol["estaño_volumen"]}, arrow_lw=0.6
)
add_year_value_annotations(
    ax_price, df, anot_years, ["precio_usd_lf"],
    {"precio_usd_lf": annotation_offsets_vol["precio_usd_lf"]},
    {"precio_usd_lf": colors_vol["precio_usd_lf"]}, arrow_lw=0.6,
    value_fmt="{:,.1f}"
)

# tasas de crecimiento
add_period_growth_annotations_multi(
    ax_v, df, growth_periods, cols_vol,
    period_growth_offsets_vol, colors_vol, abbr_vol,
    line_spacing_ratio=0.01
)

# ejes y leyendas
ax_v.set_title(f"Estaño: Volumen vs. Precio ({df.index[0]}–{df.index[-1]})",
               fontweight="bold")
ax_v.set_xlabel("Año")
ax_v.set_ylabel("Volumen (kg finos)", color=colors_vol["estaño_volumen"])
ax_price.set_ylabel("Precio (USD por libra fina)", color=colors_vol["precio_usd_lf"])
ax_v.tick_params(axis="y", labelcolor=colors_vol["estaño_volumen"])
ax_price.tick_params(axis="y", labelcolor=colors_vol["precio_usd_lf"])
ax_v.set_xticks(df.index[::max(1, len(df)//31)])
ax_v.tick_params(axis="x", rotation=45)

# leyenda combinada
h1,l1 = ax_v.get_legend_handles_labels()
h2,l2 = ax_price.get_legend_handles_labels()
ax_v.legend(h1+h2, l1+l2, loc="upper left", fontsize=11)

plt.tight_layout()
plt.savefig(os.path.join(output_dir,"estanio_volumen_precio_dual_axis.png"), dpi=300)
plt.show()
 
