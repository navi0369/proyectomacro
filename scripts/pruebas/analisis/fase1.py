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
import seaborn as sns

# %%
conn=sqlite3.connect("../../db/proyectomacro.db")
df_tasa=pd.read_sql("SELECT * FROM Tasa_Crecimiento_PIB",conn)
df_precios_minerales=pd.read_sql_query('SELECT año,zinc,estaño,plata,oro FROM precio_oficial_minerales where año>1955 and año<2024',conn)
df_precios_petroleo=pd.read_sql_query('SELECT año,precio as precio_petroleo FROM precio_petroleo_wti',conn)
df_reservas=pd.read_sql_query('SELECT * FROM Reservas_oro_divisas ',conn)
df_inflacion=pd.read_sql_query('SELECT * FROM inflacion_general_acumulada',conn)
conn.close()
df_reservas.head()

# %%
#juntar todos los df en uno solo y con años desde 2006 en adelante

# Unir los DataFrames por año
df = df_tasa \
    .merge(df_precios_minerales, on="año", how="inner") \
    .merge(df_precios_petroleo, on="año", how="inner") \
    .merge(df_reservas, on="año", how="inner") \
    .merge(df_inflacion, on="año", how="inner")
# Filtrar registros desde 2006 en adelante
df = df[df["año"] >= 2006]

# Mostrar los primeros registros

# %%
from statsmodels.tsa.stattools import grangercausalitytests
df['precio_petroleo_diff'] = df['precio_petroleo'].pct_change() * 100
df.dropna(inplace=True)
grangercausalitytests(df[['crecimiento', 'precio_petroleo_diff']], maxlag=1)

# %%
for col in ['zinc', 'estaño', 'oro', 'plata', 'precio_petroleo']:
    df[f'{col}_lag1'] = df[col].shift(1)
    df[f'{col}_lag2'] = df[col].shift(2)
df.dropna(inplace=True)

# %%
variables_rezagadas = ['zinc_lag1', 'zinc_lag2', 
                       'estaño_lag1', 'estaño_lag2', 
                       'oro_lag1', 'oro_lag2', 
                       'plata_lag1', 'plata_lag2', 
                       'precio_petroleo_lag1', 'precio_petroleo_lag2']

correlaciones_crecimiento = df[['crecimiento'] + variables_rezagadas].corr()
correlaciones_crecimiento = correlaciones_crecimiento[['crecimiento']].drop('crecimiento')

sns.heatmap(correlaciones_crecimiento, annot=True, cmap='coolwarm')
plt.title("Correlación: Crecimiento PIB vs Precios Rezagados")
plt.show()

# %%
correlaciones_inflacion = df[['inflacion', *variables_rezagadas]].corr()
correlaciones_inflacion = correlaciones_inflacion[['inflacion']].drop('inflacion')

sns.heatmap(correlaciones_inflacion, annot=True, cmap='coolwarm')
plt.title("Correlación: Inflación vs Precios Rezagados")
plt.show()


# %%
correlaciones_reservas = df[['reservas_totales', *variables_rezagadas]].corr()
correlaciones_reservas = correlaciones_reservas[['reservas_totales']].drop('reservas_totales')

sns.heatmap(correlaciones_reservas, annot=True, cmap='coolwarm')
plt.title("Correlación: Reservas vs Precios Rezagados")
plt.show()


# %%
from statsmodels.tsa.stattools import adfuller
df["precio_petroleo_diff"] = df["precio_petroleo"].pct_change() * 100
df = df.dropna()
def adf_test(series):
    result = adfuller(series.dropna())
    return {"ADF Statistic": result[0], "p-value": result[1]}
adf_test(df["crecimiento"])


# %%
from statsmodels.tsa.stattools import grangercausalitytests

grangercausalitytests(df[['crecimiento', 'precio_petroleo_diff']], maxlag=1)

