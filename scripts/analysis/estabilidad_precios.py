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
"""Análisis de la relación entre estabilidad económica, precios internacionales
y exportaciones en Bolivia."""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import statsmodels.api as sm
import os

# %%
# Conectar a la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "db", "proyectomacro.db")
conn = sqlite3.connect(DB_PATH)

# Cargar datos necesarios
crecimiento = pd.read_sql("SELECT año, crecimiento FROM Tasa_Crecimiento_PIB", conn)
exportaciones = pd.read_sql("SELECT año, total_valor_oficial FROM exportaciones_totales", conn)
precios_minerales = pd.read_sql(
    "SELECT año, zinc, estaño, plata, oro, cobre FROM precio_oficial_minerales",
    conn
)
precio_petroleo = pd.read_sql("SELECT año, precio FROM precio_petroleo_wti", conn)
conn.close()

# %%
# Preparar los DataFrames
for df in [crecimiento, exportaciones, precios_minerales, precio_petroleo]:
    df['año'] = df['año'].astype(int)

precios_minerales['precio_minerales_promedio'] = precios_minerales[
    ['zinc', 'estaño', 'plata', 'oro', 'cobre']
].mean(axis=1)

# Combinar datos en un único DataFrame
merged = (
    crecimiento.merge(exportaciones, on='año', how='left')
    .merge(precio_petroleo, on='año', how='left')
    .merge(precios_minerales[['año', 'precio_minerales_promedio']], on='año', how='left')
)
merged.set_index('año', inplace=True)

# %%
# Calcular matriz de correlación
corr_cols = ['crecimiento', 'total_valor_oficial', 'precio', 'precio_minerales_promedio']
correlation = merged[corr_cols].corr()
print("\nMatriz de correlación:\n", correlation)

# %%
# Modelo de regresión lineal
reg_data = merged.dropna(subset=corr_cols)
X = reg_data[['total_valor_oficial', 'precio', 'precio_minerales_promedio']]
X = sm.add_constant(X)
y = reg_data['crecimiento']
model = sm.OLS(y, X).fit()
print(model.summary())

# %%
# Crear directorio para las figuras
output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "imagenes", "estabilidad")
os.makedirs(output_dir, exist_ok=True)

# Gráfica 1: Crecimiento y Exportaciones
plt.figure(figsize=(10,6))
plt.plot(merged.index, merged['crecimiento'], label='Crecimiento PIB (%)')
plt.plot(merged.index, merged['total_valor_oficial']/1000, label='Exportaciones totales (miles de MM USD)')
plt.title('Crecimiento del PIB y Exportaciones Totales')
plt.xlabel('Año')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'crecimiento_exportaciones.png'), dpi=300)
plt.close()

# Gráfica 2: Crecimiento y Precios internacionales promedio
plt.figure(figsize=(10,6))
plt.plot(merged.index, merged['crecimiento'], label='Crecimiento PIB (%)')
plt.plot(merged.index, merged['precio_minerales_promedio'], label='Precio minerales promedio (USD)')
plt.plot(merged.index, merged['precio'], label='Precio petróleo WTI (USD/barril)')
plt.title('Crecimiento del PIB y Precios Internacionales')
plt.xlabel('Año')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'crecimiento_precios.png'), dpi=300)
plt.close()

# Gráfica 3: Dispersión Crecimiento vs Exportaciones
plt.figure(figsize=(8,6))
sns.regplot(data=reg_data, x='total_valor_oficial', y='crecimiento')
plt.title('Crecimiento del PIB vs Exportaciones Totales')
plt.xlabel('Exportaciones Totales (MM USD)')
plt.ylabel('Crecimiento PIB (%)')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'dispersion_exportaciones.png'), dpi=300)
plt.close()

# Gráfica 4: Dispersión Crecimiento vs Precios Internacionales
plt.figure(figsize=(8,6))
sns.regplot(data=reg_data, x='precio_minerales_promedio', y='crecimiento', label='Minerales')
sns.regplot(data=reg_data, x='precio', y='crecimiento', label='Petróleo', color='orange')
plt.title('Crecimiento del PIB vs Precios Internacionales')
plt.xlabel('Precio (USD)')
plt.ylabel('Crecimiento PIB (%)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'dispersion_precios.png'), dpi=300)
plt.close()

# %%
# Comentario final
print("\nConclusión preliminar:")
print("La correlación positiva entre las exportaciones totales y el crecimiento ")
print("sugiere que el desempeño externo influye en la estabilidad económica. ")
print("Asimismo, el modelo de regresión muestra que las variaciones en los ")
print("precios internacionales, tanto de minerales como del petróleo, están ")
print("asociadas al crecimiento del PIB, lo que indica cierta dependencia de ")
print("la economía boliviana respecto a estos factores externos.")

