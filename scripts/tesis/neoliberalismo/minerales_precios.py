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
import sqlite3
import os

# ------------------------------------------------------------------
# 1. RUTAS
# ------------------------------------------------------------------
base_path    = "../../../assets/tesis/neoliberalismo/serie_completa"
dir_completa = os.path.join(base_path, "precios_minerales")
os.makedirs(dir_completa, exist_ok=True)

# ------------------------------------------------------------------
# 2. ESTILO
# ------------------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family'    : 'serif',
    'font.size'      : 12,
    'axes.titlesize' : 16,
    'axes.labelsize' : 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'grid.linestyle' : '--',
    'lines.linewidth': 2,
    'figure.dpi'     : 150,
    'savefig.bbox'   : 'tight'
})

# ------------------------------------------------------------------
# 3. DATOS
# ------------------------------------------------------------------
conn = sqlite3.connect('../../../db/proyectomacro.db')
df = pd.read_sql_query("SELECT * FROM precio_oficial_minerales", conn)
conn.close()

df.set_index('año', inplace=True)
df = df.loc[1982:2002]

minerales = [
    'zinc','estaño','oro','plata','antimonio',
    'plomo','wolfram','cobre','bismuto'
]

# ------------------------------------------------------------------
# 4. AYUDAS
# ------------------------------------------------------------------
def estad_crisis(s):
    mean = s.loc[1982:1986].mean()
    delta= (s.loc[1986] - s.loc[1982]) / s.loc[1982] * 100
    return f"Crisis (82‑86)\nMean: {mean:.2f}\nΔ86/82: {delta:.1f}%"

def estad_post(s):
    mean = s.loc[1986:2002].mean()
    delta= (s.loc[2002] - s.loc[1986]) / s.loc[1986] * 100
    return f"Post (86‑02)\nMean: {mean:.2f}\nΔ2002/86: {delta:.1f}%"

# offsets específicos para no solapar anotaciones
annotation_offsets = {
    'zinc':    {1982:(0,  1.2), 1986:(0,  1.1), 2002:(0, 0.8)},
    'estaño':  {1982:(0,  0.95), 1986:(0,  0.90), 2002:(0, 1.09)},
    'oro':     {1982:(0,  1.05), 1986:(0,  1.05),2002:(0, 0.92)},
    'plata':   {1982:(0,  0.93), 1986:(0,  1.1), 2002:(0, 0.9)},
    'antimonio':{1982:(0, 1.13),1986:(0, 1.1),2002:(0, 1.1)},
    'plomo':   {1982:(0,  1.05), 1986:(0,  1.18), 2002:(0, 0.95)},
    'wolfram': {1982:(0,  1.05), 1986:(0,  1.1), 2002:(0, 0.87)},
    'cobre':   {1982:(0,  1.08), 1986:(0,  1.10), 2002:(0, 0.9)},
    'bismuto': {1982:(0,  1.15),1986:(0, 0.9),2002:(0, 0.9)},
}
# Posición para cuadros estadísticos por mineral
x_y_for_text = {
    'zinc':    {'crisis': (1984, 0.95), 'post': (1991, 0.95)},
    'estaño':  {'crisis': (1985, 0.95), 'post': (1991, 0.95)},
    'oro':     {'crisis': (1984, 0.95), 'post': (1991, 0.95)},
    'plata':   {'crisis': (1984, 0.95), 'post': (1991, 0.95)},
    'antimonio':{'crisis': (1984, 0.95), 'post': (1991, 0.95)},
    'plomo':   {'crisis': (1984, 0.95), 'post': (1991.5, 0.95)},
    'wolfram': {'crisis': (1984, 0.95), 'post': (1991, 0.95)},
    'cobre':   {'crisis': (1984, 0.95), 'post': (1991, 0.95)},
    'bismuto': {'crisis': (1984, 0.95), 'post': (1991, 0.95)},
}

# ------------------------------------------------------------------
# 5. BUCLE DE GRAFICACIÓN
# ------------------------------------------------------------------
for m in minerales:
    if m not in df.columns:
        continue
    serie = df[m].dropna()
    if serie.empty:
        continue

    crisis = serie.loc[1982:1986]
    post   = serie.loc[1986:2002]

    fig, ax = plt.subplots(figsize=(10, 6))

    # tramo Crisis (82‑86)
    ax.plot(crisis.index, crisis, color='crimson', label='Crisis (82‑86)')
    # tramo Post‑crisis (86‑02)
    ax.plot(post.index,   post,   color='#1f77b4', label='Post Crisis (86‑02)')

    # línea divisoria en 1986
    ax.axvline(1986, color='gray', linestyle='--', linewidth=1)

    # anotaciones: primer, corte, último año
    for yr in (1982, 1986, 2002):
        if yr not in serie.index:
            continue
        val = serie.loc[yr]
        dx, dy_factor = annotation_offsets.get(m, {}).get(yr, (0, 1.05))
        ax.annotate(f"{val:.2f}",
                    xy=(yr, val),
                    xytext=(yr + dx, val * dy_factor),
                    arrowprops=dict(arrowstyle='->'),
                    ha='center', fontsize=11)
    # cuadros estadísticos
    x_c, y_c = x_y_for_text.get(m, {}).get('crisis', (1984, 0.95))
    x_p, y_p = x_y_for_text.get(m, {}).get('post', (1996, 0.95))

    ax.text(x_c, serie.max()*y_c, estad_crisis(serie),
            fontsize=10, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))

    ax.text(x_p, serie.max()*y_p, estad_post(serie),
            fontsize=10, bbox=dict(facecolor='white', alpha=0.8, edgecolor='black'))


    # formato final
    ax.set_title(f"Precio Oficial de {m.capitalize()} (1982‑2002)", fontweight='bold')
    ax.set_xlabel("Año")
    ax.set_ylabel("Precio (USD)")
    ax.set_xlim(1981, 2003)
    ax.set_xticks(range(1982, 2003))
    ax.tick_params(labelrotation=45)
    ax.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig(os.path.join(dir_completa, f"precio_{m}.png"))
    plt.close(fig)

