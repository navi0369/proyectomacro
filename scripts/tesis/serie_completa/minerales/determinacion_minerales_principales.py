# ---
# jupyter:
#   jupytext:
#     formats: notebooks/tesis/serie_completa///ipynb,scripts/tesis/serie_completa///py:percent
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
from config import DB_PATH
from tesis import apply_mpl_style
apply_mpl_style()

import pandas as pd
import sqlite3

conn = sqlite3.connect(DB_PATH, uri=True)
df_exportaciones_tradicionales_minerales = pd.read_sql_query("SELECT año, minerales FROM exportaciones_tradicionales", conn)
df_produccion_minerales = pd.read_sql_query("SELECT * FROM exportaciones_minerales_totales where año>1991", conn)
valor_cols = [c for c in df_produccion_minerales.columns if c.endswith('_valor')]
df_produccion_minerales[valor_cols]=df_produccion_minerales[valor_cols]/1000

conn.close()

df_exportaciones_tradicionales_minerales


df_produccion_minerales

total_por_mineral = df_produccion_minerales[valor_cols].sum()


top4 = total_por_mineral.sort_values(ascending=False).head(4)