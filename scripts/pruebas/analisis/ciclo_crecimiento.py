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
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import libsql_experimental as libsql
import os
from dotenv import load_dotenv


# %%
load_dotenv()
url = os.getenv("TURSO_DATABASE_URL")
auth_token = os.getenv("TURSO_AUTH_TOKEN")
conn = libsql.connect("proyectomacro.db", sync_url=url, auth_token=auth_token)
cursor = conn.cursor()
conn.sync()

# %%
df=pd.read_sql_query('select * from tasa_crecimiento_pib',conn)
df.set_index("Año", inplace=True)  # Convertir Año en índice de tiempo
df

# %%
# Descomposición de la serie de tiempo
descomposicion = sm.tsa.seasonal_decompose(df["Crecimiento"], model="additive", period=10)
descomposicion.plot()
plt.show()


# %%
import matplotlib.pyplot as plt
from statsmodels.tsa.filters.hp_filter import hpfilter

# Aplicar el filtro HP con lambda=100
ciclo_100, tendencia_100 = hpfilter(df["Crecimiento"], lamb=100)

# Configuración del estilo profesional
plt.figure(figsize=(12,6))

# Graficar la serie original, la tendencia y el ciclo
plt.plot(df.index, df["Crecimiento"], label="Tasa de Crecimiento del PIB", color='blue', alpha=0.6, linewidth=2)
plt.plot(df.index, tendencia_100, label="Tendencia (λ=100)", color='red', linestyle="--", linewidth=2)
plt.plot(df.index, ciclo_100, label="Ciclo Económico (λ=100)", color='green', linestyle=":", linewidth=2)
plt.axhline(0, color="black", linestyle="--", linewidth=1.5)

# Añadir título y etiquetas
plt.title("Filtro Hodrick-Prescott (λ=100)")
plt.xlabel("Fecha")
plt.ylabel("Tasa de Crecimiento")
plt.legend(loc="best")
plt.tight_layout()
plt.show()


# %%
import matplotlib.pyplot as plt
from statsmodels.tsa.filters.hp_filter import hpfilter

# Aplicar el filtro HP con lambda=100
ciclo_100, tendencia_100 = hpfilter(df["Crecimiento"], lamb=100)

# Configurar estilo vistoso
plt.figure(figsize=(12,6))

# Graficar la serie original, la tendencia y el ciclo
plt.plot(df.index, df["Crecimiento"], label="Tasa de Crecimiento del PIB", color='blue', alpha=0.75, linewidth=2)
plt.plot(df.index, tendencia_100, label="Tendencia (λ=100)", color='red', linestyle="--", linewidth=2.5)
plt.axhline(0, color="black", linestyle="--", linewidth=1.5)

# Títulos y etiquetas con formato
plt.title("Filtro Hodrick-Prescott (λ=100)", fontsize=16, fontweight='bold')
plt.xlabel("Fecha", fontsize=14)
plt.ylabel("Tasa de Crecimiento", fontsize=14)
plt.legend(loc="best", fontsize=12)
plt.xticks(df.index[::2], rotation=45)
plt.grid()
plt.show()


# %%

# Aplicar el filtro HP con lambda=1600
ciclo_1600, tendencia_1600 = hpfilter(df["Crecimiento"], lamb=160)

# Configurar estilo vistoso
plt.figure(figsize=(12,6))

# Graficar la serie original, la tendencia y el ciclo
plt.plot(df.index, df["Crecimiento"], label="Tasa de Crecimiento del PIB", color='blue', alpha=0.75, linewidth=2)
plt.plot(df.index, tendencia_1600, label="Tendencia (λ=160)", color='red', linestyle="--", linewidth=2.5)
plt.axhline(0, color="black", linestyle="--", linewidth=1.5)

# Títulos y etiquetas con formato
plt.title("Filtro Hodrick-Prescott (λ=160)", fontsize=16, fontweight='bold')
plt.xlabel("Fecha", fontsize=14)
plt.ylabel("Tasa de Crecimiento", fontsize=14)
plt.legend(loc="best", fontsize=12)
plt.xticks(df.index[::2], rotation=45)
plt.tight_layout()
plt.grid()
plt.show()


# %%
import pandas as pd

# Datos de 2016 a 2023 (convertidos de notación española a float)
years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

zinc       = [0.93, 1.30, 1.33, 1.16, 1.02, 1.35, 1.59, 1.35]
estano     = [7.38, 7.99, 9.14, 9.13, 8.50, 7.72, 14.58, 14.58]
oro        = [1245.28, 1252.07, 1269.12, 1382.60, 1754.51, 1803.74, 1800.51, 1803.74]
plata      = [17.02, 17.04, 15.71, 16.09, 20.18, 25.29, 21.72, 25.29]
antimonio  = [6335.41, 8175.86, 8201.28, 6682.08, 5763.39, 10661.46, 12918.33, 10661.46]
plomo      = [0.84, 1.04, 1.02, 0.91, 0.83, 0.99, 0.98, 0.99]
wolfram    = [105.27, 134.90, 164.32, 129.47, 123.46, 159.49, 173.86, 159.49]
cobre      = [2.19, 2.77, 2.96, 2.72, 2.77, 4.19, 4.02, 4.19]
bismuto    = [4.29, 4.75, 4.40, 3.06, 2.61, 3.58, 3.77, 3.58]
cadmio     = [0.57, 0.74, 1.24, 1.17, 1.00, 1.11, 1.46, 1.11]
hierro     = [58.22, 71.45, 69.95, 92.60, 105.64, 92.60, 120.79, 162.56]
manganeso  = [4.27, 6.02, 7.23, 5.71, 4.69, 5.03, 6.09, 5.03]

# Crear DataFrame con los datos
data = {
    "Año": years,
    "Zinc": zinc,
    "Estaño": estano,
    "Oro": oro,
    "Plata": plata,
    "Antimonio": antimonio,
    "Plomo": plomo,
    "Wolfram": wolfram,
    "Cobre": cobre,
    "Bismuto": bismuto,
    "Cadmio": cadmio,
    "Hierro": hierro,
    "Manganeso": manganeso
}

df_minerales = pd.DataFrame(data)
df_minerales
