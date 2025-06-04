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
import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %%
conn = sqlite3.connect("../../db/proyectomacro.db")
cursor = conn.cursor()

# %%
df=pd.read_sql_query('SELECT * FROM PIB_Real_Gasto',conn)
conn.close()
df.set_index('año',inplace=True)
df_participacion=pd.DataFrame({
    'ct':df['gastos_consumo']/df['pib_real_base_1990'],
    'i':df['formacion_capital']/df['pib_real_base_1990'],
    'x':df['exportacion_bienes_servicios']/df['pib_real_base_1990'],
    'm':df['importacion_bienes']/df['pib_real_base_1990'],
    'c':df['consumo_privado']/df['pib_real_base_1990'],
    'g':df['consumo_publico']/df['pib_real_base_1990']
})
df_participacion.loc[1950:1956]

# %%
## Dividir el DataFrame en los tres periodos históricos
df_periodo1 = df_participacion.loc[1952:1984]
df_periodo2 = df_participacion.loc[1985:2005]
df_periodo3 = df_participacion.loc[2006:2025]

# Calcular estadísticas descriptivas relevantes
stats_periodo1 = df_periodo1.describe().T[['mean', 'std', 'min', 'max']]
stats_periodo2 = df_periodo2.describe().T[['mean', 'std', 'min', 'max']]
stats_periodo3 = df_periodo3.describe().T[['mean', 'std', 'min', 'max']]

# Crear un DataFrame consolidado con las estadísticas de cada periodo
df_stats = pd.concat([stats_periodo1, stats_periodo2, stats_periodo3], axis=1)
df_stats.columns = pd.MultiIndex.from_product(
    [['1952-1984', '1985-2005', '2006-2025'], ['mean', 'std', 'min', 'max']]
)
df_stats


# %%
# Definir directorio de salida y crearlo si no existe
output_dir = "../../assets/imagenes"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# Dividir el DataFrame en tres periodos históricos
periodos = {
    '1952-1974': df_participacion.loc[1952:1974],
    '1975-2005': df_participacion.loc[1975:2005],
    '2006-2025': df_participacion.loc[2006:2025]
}

# Columnas de interés
cols = ['ct', 'c', 'g', 'i', 'x', 'm']

# Calcular estadísticas descriptivas para cada periodo
stats_dict = {}
for periodo, dfp in periodos.items():
    stats = dfp[cols].describe().T[['mean', 'std', 'min', 'max']]
    stats_dict[periodo] = stats

df_stats = pd.concat(stats_dict, axis=1)
df_stats.columns = pd.MultiIndex.from_product([list(stats_dict.keys()), ['mean', 'std', 'min', 'max']])
print(df_stats)

# Además, para las anotaciones en la gráfica, calculamos las medias (puedes ajustar los periodos según convenga)
media_p1 = {
    'c': periodos['1952-1974']['c'].mean(),
    'g': periodos['1952-1974']['g'].mean(),
    'ct': periodos['1952-1974']['ct'].mean(),
    'i': periodos['1952-1974']['i'].mean(),
    'x': periodos['1952-1974']['x'].mean(),
    'm': periodos['1952-1974']['m'].mean()
}
media_p2 = {
    'c': periodos['1975-2005']['c'].mean(),
    'g': periodos['1975-2005']['g'].mean(),
    'ct': periodos['1975-2005']['ct'].mean(),
    'i': periodos['1975-2005']['i'].mean(),
    'x': periodos['1975-2005']['x'].mean(),
    'm': periodos['1975-2005']['m'].mean()
}
media_p3 = {
    'c': periodos['2006-2025']['c'].mean(),
    'g': periodos['2006-2025']['g'].mean(),
    'ct': periodos['2006-2025']['ct'].mean(),
    'i': periodos['2006-2025']['i'].mean(),
    'x': periodos['2006-2025']['x'].mean(),
    'm': periodos['2006-2025']['m'].mean()
}

# Definir textos para las anotaciones (ejemplo usando medias de consumo privado, público, total, inversión, exportaciones e importaciones)
text_p1 = (
    "Medias en el periodo 1952-1984\n"
    f"Media C: {media_p1['c']:.2f}\n"
    f"Media G: {media_p1['g']:.2f}\n"
    f"Media CT: {media_p1['ct']:.2f}\n"
    f"Media I: {media_p1['i']:.2f}\n"
    f"Media X: {media_p1['x']:.2f}\n"
    f"Media M: {media_p1['m']:.2f}"
)
text_p2 = (
    "Medias en el periodo 1985-2005\n"
    f"Media C: {media_p2['c']:.2f}\n"
    f"Media G: {media_p2['g']:.2f}\n"
    f"Media CT: {media_p2['ct']:.2f}\n"
    f"Media I: {media_p2['i']:.2f}\n"
    f"Media X: {media_p2['x']:.2f}\n"
    f"Media M: {media_p2['m']:.2f}"
)
text_p3 = (
    "Medias en el periodo 2006-2025\n"
    f"Media C: {media_p3['c']:.2f}\n"
    f"Media G: {media_p3['g']:.2f}\n"
    f"Media CT: {media_p3['ct']:.2f}\n"
    f"Media I: {media_p3['i']:.2f}\n"
    f"Media X: {media_p3['x']:.2f}\n"
    f"Media M: {media_p3['m']:.2f}"
)

# Crear la gráfica
fig, ax = plt.subplots(figsize=(12, 8))

# Para la gráfica, se puede usar stackplot para las áreas. 
# Considera que el consumo total (ct) es la suma de consumo privado (c) y público (g).
# Aquí mostramos el desglose del consumo (c y g) junto a inversión, exportaciones e importaciones.
ax.stackplot(df_participacion.index,
             df_participacion['c'],
             df_participacion['g'],
             df_participacion['i'],
             df_participacion['x'],
             df_participacion['m'],
             labels=['Consumo Privado (c)', 'Consumo Público (g)', 'Inversión (i)', 'Exportaciones (x)', 'Importaciones (m)'])

# También se puede superponer una línea para el Consumo Total (ct), que debería igualar c+g.
ax.plot(df_participacion.index, df_participacion['ct'], color='black', lw=2, label='Consumo Total (ct)')

ax.set_xlabel('Año')
ax.set_ylabel('Participación sobre PIB Real (base 1990)')
ax.set_title('Evolución de los Componentes del PIB (Participaciones)')
ax.legend(loc='upper left')
ax.set_xticks(df_participacion.index[::2])
ax.set_xticklabels(df_participacion.index[::2], rotation=45)

# Configurar propiedades del recuadro para las anotaciones
bbox_props = dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8)

# Agregar las anotaciones para cada periodo en posiciones escogidas (ajusta las coordenadas según convenga)
ax.text(1960, 0.3, text_p1, fontsize=10, color='black', bbox=bbox_props, ha='center')
ax.text(1995, 0.3, text_p2, fontsize=10, color='black', bbox=bbox_props, ha='center')
ax.text(2015, 0.3, text_p3, fontsize=10, color='black', bbox=bbox_props, ha='center')

# Sombrear los periodos históricos
ax.axvspan(1952, 1984, facecolor='lightblue', alpha=0.21)
ax.axvspan(1985, 2005, facecolor='lightgreen', alpha=0.25)
ax.axvspan(2006, 2025, facecolor='lightcoral', alpha=0.21)

plt.tight_layout()
plt.figtext(0.5, -0.005, "Fuente: Elaboración propia en base a datos de la INE", ha="center", fontsize=12, color='black')
plt.savefig(os.path.join(output_dir, ), bbox_inches='tight', dpi=300)
plt.show()
plt.close()
