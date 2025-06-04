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
import libsql_experimental as libsql
from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# %%
load_dotenv()
url = os.getenv("TURSO_DATABASE_URL")
auth_token = os.getenv("TURSO_AUTH_TOKEN")
conn = libsql.connect("proyectomacro.db", sync_url=url, auth_token=auth_token)
cursor = conn.cursor()
conn.sync()

# %%
df=pd.read_sql_query('select * from balanza_comercial',conn)
# La lista de exportaciones de 1992 a 2024:
Exportaciones = [
    741.1, 785.8, 1089.8, 1137.6, 1214.5, 1253.9, 1108.1, 1042.2, 
    1246.3, 1226.2, 1319.9, 1589.8, 2194.6, 2867.4, 4088.3, 4821.8, 
    6932.9, 5399.6, 6966.1, 9145.8, 11814.6, 12251.7, 12899.1, 8737.1, 
    7126.3, 8223.1, 9014.7, 8804.9, 6974.7, 11165.2, 13856.3, 10806.0, 8923.0
]

# Crear un dataframe con los datos de la lista, asignándoles el rango de años de 1992 a 2024:
years_new = list(range(1992, 2025))
df_new = pd.DataFrame({
    'Año': years_new,
    'Exportaciones': Exportaciones
})

# Concatenar el dataframe original con el nuevo:
df_concat = pd.concat([df, df_new], ignore_index=True)

# Ordenar por 'Año'
df_concat = df_concat.sort_values('Año')

# Para los años en conflicto (1992-2004), usamos los datos del df_new.
# Esto se puede hacer agrupando por 'Año' y tomando la última entrada de cada grupo.
df_final = df_concat.groupby('Año', as_index=False).last()

# df_final tendrá la columna 'Exportaciones' con datos desde 1949 hasta 2024.
df_final.tail(30)

# %%
# Calcular los retornos logarítmicos interanuales
log_returns = np.diff(np.log(df_final['Exportaciones']))

# Calcular la volatilidad como la desviación estándar muestral de los retornos
volatilidad = np.std(log_returns, ddof=1)

print("Volatilidad anual (desviación estándar de los retornos logarítmicos):", volatilidad)

# %%
# Calcular volatilidad móvil en ventanas de 5 años
df_final["Volatilidad_Movil"] = df_final["Exportaciones"].pct_change().rolling(window=5).std()
plt.figure(figsize=(10, 5))
plt.plot(df_final["Año"], df_final["Volatilidad_Movil"], marker='o', linestyle='-', color='r')

plt.xlabel("Año")
plt.ylabel("Volatilidad Móvil (Desviación Std)")
plt.title("Volatilidad de Exportaciones a lo Largo del Tiempo (Rolling 5 años)")
plt.grid(True)
plt.show()


