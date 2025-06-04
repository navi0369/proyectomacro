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

# Supongamos que ya lo convertiste a CSV y cargaste así:
df = pd.read_csv("/home/navi/Downloads/datos/precio_petroleo.csv")

# Asegurate de tener columnas como: 'AÑO', 'MES', 'GLP_50_50_cUSGal', 'GLP_50_50_US_Bbl', etc.

# Agrupar por año y calcular promedio anual
df

