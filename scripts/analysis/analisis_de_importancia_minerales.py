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
import sqlite3
import matplotlib.pyplot as plt
conn = sqlite3.connect("../../db/proyectomacro.db")
df = pd.read_sql("SELECT * FROM exportaciones_minerales_totales", conn)
df.set_index('año', inplace=True)
df.index = df.index.astype(int)
conn.close()
df.tail()

# %%
# Seleccionar solo las columnas de valor (miles de USD)
valor_columns = [col for col in df.columns if 'valor' in col]

# Filtrar los datos por periodo
df_87_06 = df.loc[1987:2006, valor_columns]
df_06_final = df.loc[2006:, valor_columns]

# Sumar el valor total por mineral en cada periodo
total_valores_87_06 = df_87_06.sum().sort_values(ascending=False)
total_valores_06_final = df_06_final.sum().sort_values(ascending=False)

# Renombrar los índices para mayor claridad
total_valores_87_06.index = total_valores_87_06.index.str.replace('_valor', '').str.capitalize()
total_valores_06_final.index = total_valores_06_final.index.str.replace('_valor', '').str.capitalize()

# Gráfico 1987-2006
plt.figure(figsize=(10, 5))
plt.bar(total_valores_87_06.index, total_valores_87_06, color='skyblue', edgecolor='black')
plt.title('Valor Total Exportado por Mineral (1987-2006)')
plt.ylabel('USD')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico 2006-final
plt.figure(figsize=(10, 5))
plt.bar(total_valores_06_final.index, total_valores_06_final, color='salmon', edgecolor='black')
plt.title('Valor Total Exportado por Mineral (2006-Final)')
plt.ylabel('USD')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
# Calcular la participación anual
participacion_87_06 = df_87_06.div(df_87_06.sum(axis=1), axis=0) * 100
participacion_06_final = df_06_final.div(df_06_final.sum(axis=1), axis=0) * 100

# Obtener el mineral dominante en cada año
mineral_dominante_87_06 = participacion_87_06.idxmax(axis=1).str.replace('_valor', '').str.capitalize()
mineral_dominante_06_final = participacion_06_final.idxmax(axis=1).str.replace('_valor', '').str.capitalize()

# Graficar para 1987-2006
plt.figure(figsize=(10, 5))
mineral_dominante_87_06.value_counts().sort_index().plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Frecuencia del Mineral Dominante por Año (1987-2006)')
plt.ylabel('Número de Años como Líder')
plt.xticks(rotation=45)
plt.show()

# Graficar para 2006-final
plt.figure(figsize=(10, 5))
mineral_dominante_06_final.value_counts().sort_index().plot(kind='bar', color='salmon', edgecolor='black')
plt.title('Frecuencia del Mineral Dominante por Año (2006-Final)')
plt.ylabel('Número de Años como Líder')
plt.xticks(rotation=45)
plt.show()

# %%
# Calcular crecimiento relativo entre los períodos
crecimiento = ((total_valores_06_final - total_valores_87_06) / total_valores_87_06) * 100

# Graficar el crecimiento relativo
plt.figure(figsize=(10, 5))
crecimiento.plot(kind='bar', color='green', edgecolor='black')
plt.title('Crecimiento de Exportaciones por Mineral (1987-2006 vs 2006-Final)')
plt.ylabel('Crecimiento (%)')
plt.xticks(rotation=45)
plt.axhline(y=0, color='black', linestyle='--')
plt.show()

