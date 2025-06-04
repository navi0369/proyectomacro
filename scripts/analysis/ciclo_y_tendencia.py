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

# %%
conn=sqlite3.connect('../../db/proyectomacro.db')
df=pd.read_sql_query("SELECT * FROM Tasa_Crecimiento_PIB ",conn)
df.set_index('año',inplace=True)
df.columns

# %%

# Visualización de la tasa de crecimiento a lo largo de los años
df['crecimiento'].plot(figsize=(10, 6))
plt.title('Tasa de Crecimiento del PIB')
plt.xlabel('Año')
plt.ylabel('Crecimiento (%)')
plt.axhline(y=0, color='red', linestyle='--', label='Línea en y=0')
plt.show()

# %%
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Graficar ACF (Autocorrelación)
plt.figure(figsize=(12, 6))
plt.subplot(121)
plot_acf(df['crecimiento'], lags=15, ax=plt.gca())

# Graficar PACF (Autocorrelación Parcial)
plt.subplot(122)
plot_pacf(df['crecimiento'], lags=15, ax=plt.gca())  # Reducir el número de lags

plt.show()

# %%
from statsmodels.tsa.arima.model import ARIMA

# Suponiendo que seleccionamos p=1, d=1, q=1 (puedes ajustar estos valores)
model = ARIMA(df['crecimiento'], order=(1, 1, 1))
model_fit = model.fit()

# Ver resumen del modelo
print(model_fit.summary())

# %%
df
