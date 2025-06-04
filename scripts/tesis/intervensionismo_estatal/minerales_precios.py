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

# ------------------------------------------------------------------ 1. rutas
base_path    = "../../../assets/tesis/intervensionismo_estatal/serie_completa"
dir_completa = os.path.join(base_path, "precios_minerales")
os.makedirs(dir_completa, exist_ok=True)

# ------------------------------------------------------------------ 2. estilo
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family':'serif','font.size':12,'axes.titlesize':16,'axes.labelsize':14,
    'xtick.labelsize':12,'ytick.labelsize':12,'grid.linestyle':'--',
    'lines.linewidth':2,'figure.dpi':150,'savefig.bbox':'tight'
})

# ------------------------------------------------------------------ 3. datos
conn = sqlite3.connect('../../../db/proyectomacro.db')
df = pd.read_sql_query("SELECT * FROM precio_oficial_minerales", conn)
conn.close()

df.set_index('año', inplace=True)
df = df.loc[1951:1982]                 #     ahora hay datos desde 1951

minerales = ['zinc','estaño','plata','antimonio','plomo','wolfram','cobre','bismuto']

# ------------------------------------------------------------------ 4. ayudas
def estad_post(s):
    mean = s.loc[1956:1982].mean()
    g82  = (s.loc[1982] - s.loc[1956]) / s.loc[1956] * 100
    return f"Post (56‑82)\nMean: {mean:.2f}\nΔ82/56: {g82:.1f}%"

def estad_crisis(s):
    mean = s.loc[1952:1955].mean()
    g56  = (s.loc[1956] - s.loc[1952]) / s.loc[1952] * 100
    return f"Crisis (52‑55)\nMean: {mean:.2f}\nΔ56/52: {g56:.1f}%"

offsets = {                 # factor_vertical_inicio , factor_vertical_fin
    'zinc':(1.25,0.85),'estaño':(1.25,0.85),'plata':(1.4,0.88),
    'antimonio':(1.3,0.9),'plomo':(1.3,0.9),'wolfram':(1.18,0.9),
    'cobre':(1.1,0.88),'bismuto':(1.2,0.92)
}

# ------------------------------------------------------------------ 5. bucle
for m in minerales:
    if m not in df.columns:          # columna inexistente
        continue
    serie = df[m].dropna()
    if serie.empty:                  # todo NaN
        continue

    crisis   = serie.loc[1951:1956].dropna()
    post     = serie.loc[1956:1982].dropna()
    has_cris = not serie.loc[1951:1955].dropna().empty

    fig,ax = plt.subplots(figsize=(10,6))

    # ----- crisis tramo rojo -----------------------------------------------
    if has_cris:
        ax.plot(crisis.index, crisis, color='red', label='Crisis (52‑55)')
    else:                              # p/leyenda coherente
        ax.plot([],[],color='red',label='Crisis (52‑55)')

    # ----- post‑crisis tramo azul ------------------------------------------
    ax.plot(post.index, post, color='#1f77b4', label='Post Crisis (56‑82)')

    # línea de corte
    ax.axvline(1956,color='gray',ls='--',lw=1,label='Inicio Post Crisis')

    # ----- anotaciones primer / último valor -------------------------------
    f_up,f_down = offsets[m]
    ax.annotate(f"{serie.iloc[0]:.2f}",
                xy=(serie.index[0],serie.iloc[0]),
                xytext=(serie.index[0],serie.iloc[0]*f_up),
                arrowprops=dict(arrowstyle='->'),ha='center',fontsize=11)
    if has_cris:
        ax.annotate(f"{serie.loc[1956]:.2f}",
                    xy=(serie.index[5],serie.loc[1956]),
                    xytext=(serie.index[5],serie.loc[1956]*f_up),
                    arrowprops=dict(arrowstyle='->'),ha='center',fontsize=11)
    ax.annotate(f"{serie.iloc[-1]:.2f}",
                xy=(serie.index[-1],serie.iloc[-1]),
                xytext=(serie.index[-1],serie.iloc[-1]*f_down),
                arrowprops=dict(arrowstyle='->'),ha='center',fontsize=11)

    # ----- cuadros estadísticos --------------------------------------------
    if has_cris:
        ax.text(1953 if m!='zinc' else 1957, serie.max()*0.5  , estad_crisis(serie),
                fontsize=9,bbox=dict(fc='white',alpha=0.8,ec='black'))
    ax.text(1959 if m!='zinc' else 1966, serie.max()*0.5, estad_post(serie),
            fontsize=9,bbox=dict(fc='white',alpha=0.8,ec='black'))

    # ----- estética final ---------------------------------------------------
    ax.set_title(f"Precio oficial de {m.capitalize()} (1951‑1982)",
                 fontweight='bold')
    ax.set_xlabel("Año");  ax.set_ylabel("Precio (USD)")
    ax.legend()
    plt.xticks(df.index,rotation=45)
    plt.subplots_adjust(top=0.88,bottom=0.12)

    plt.savefig(os.path.join(dir_completa,f"precio_{m}.png"))
    plt.close()

