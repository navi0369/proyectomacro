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
#     display_name: env
#     language: python
#     name: python3
# ---

# %%
import camelot
import pandas as pd

# Extraer tablas del PDF
tables = camelot.read_pdf("t.pdf", pages="all", flavor="stream")

df = tables[0].df

# Imprimir las columnas extraídas para ver cómo lucen
print("Columnas extraídas:", df.columns.tolist())

# Usar la primera fila como encabezado y eliminarla del DataFrame
df.columns = df.iloc[0]
df = df.drop(0)

# Eliminar espacios en blanco de los nombres de columna
df.columns = df.columns.str.strip()

# Imprimir nuevamente para confirmar los nombres de columna
print("Columnas ajustadas:", df.columns.tolist())

# Renombrar columnas si es necesario (ejemplo)
df.rename(columns={
    'Ppto. Aprobado': 'Ppto. Aprobado',
    'Crédito Vigente': 'Crédito Vigente'
}, inplace=True)

# Ahora filtra las columnas de interés
df



