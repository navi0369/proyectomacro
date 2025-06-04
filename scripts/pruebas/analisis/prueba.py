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
import os
conn=sqlite3.connect("../../db/proyectomacro.db")
df=pd.read_sql_query("SELECT * FROM PIB_real_Gasto", conn, index_col="año")
componentes = [
    'gastos_consumo',
    'formacion_capital',
    'exportacion_bienes_servicios',
    'importacion_bienes',
    'consumo_privado',
    'consumo_publico'
]
pct = df[componentes].div(df["pib_real_base_1990"], axis=0) * 100
pct

# %%
# 1) Con DataFrame.eval (muy legible):
pct['CIGX_minus_M'] = pct.eval(
    'gastos_consumo + formacion_capital + exportacion_bienes_servicios - importacion_bienes'
)
pct.head(30)
