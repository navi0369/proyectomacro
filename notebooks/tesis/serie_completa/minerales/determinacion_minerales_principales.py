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
import pandas as pd
import sqlite3

conn = sqlite3.connect('../../../../db/proyectomacro.db')
df_exportaciones_tradicionales_minerales = pd.read_sql_query("SELECT año, minerales FROM exportaciones_tradicionales", conn)
df_produccion_minerales = pd.read_sql_query("SELECT * FROM exportaciones_minerales_totales where año>1991", conn)
valor_cols = [c for c in df_produccion_minerales.columns if c.endswith('_valor')]
print(valor_cols)
df_produccion_minerales[valor_cols]=df_produccion_minerales[valor_cols]/1000

conn.close()

df_exportaciones_tradicionales_minerales


# %%
df_produccion_minerales

# %%
total_por_mineral = df_produccion_minerales[valor_cols].sum()
print(total_por_mineral)


# %%
top4 = total_por_mineral.sort_values(ascending=False).head(4)
print(top4)
