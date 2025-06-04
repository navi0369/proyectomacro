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
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import os

# %%
# Conectar y cargar los datos de la tabla operaciones_empresas_publicas
conn = sqlite3.connect("../../db/proyectomacro.db")
df = pd.read_sql_query("SELECT * FROM operaciones_empresas_publicas", conn)
conn.close()

# Establecer 'año' como índice (convirtiendo a entero)
df.set_index("año", inplace=True)
df.index = df.index.astype(int)

# Definir carpeta de salida para las imágenes
output_dir = "../../assets/imagenes/16.operaciones_empresas_publicas"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# --- Gráfica 1: Ingresos Totales ---
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['ingresos_totales'], marker='o', linestyle='-', color='tab:blue')
plt.title("Ingresos Totales (1990-2021)")
plt.xlabel("Año")
plt.ylabel("Ingresos Totales (% del PIB)")
plt.grid(True)
plt.xticks(df.index, rotation=45)
plt.tight_layout()
filename_ingresos = os.path.join(output_dir, "ingresos_totales.png")
plt.savefig(filename_ingresos, dpi=300)
plt.close()

# --- Gráfica 2: Egresos Totales ---
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['egresos_totales'], marker='s', linestyle='-', color='tab:red')
plt.title("Egresos Totales (1990-2021)")
plt.xlabel("Año")
plt.ylabel("Egresos Totales (% del PIB)")
plt.grid(True)
plt.xticks(df.index, rotation=45)
plt.tight_layout()
filename_egresos = os.path.join(output_dir, "egresos_totales.png")
plt.savefig(filename_egresos, dpi=300)
plt.close()

# --- Gráfica 3: Resultado Fiscal Global ---
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['resultado_fiscal_global'], marker='^', linestyle='-', color='tab:green')
plt.title("Resultado Fiscal Global (1990-2021)")
plt.xlabel("Año")
plt.ylabel("Resultado Fiscal Global (% del PIB)")
plt.grid(True)
plt.xticks(df.index, rotation=45)
plt.tight_layout()
filename_resultado = os.path.join(output_dir, "resultado_fiscal_global.png")
plt.savefig(filename_resultado, dpi=300)
plt.close()

# --- Gráfica Combinada: Subplots ---
fig, axs = plt.subplots(3, 1, figsize=(12, 18), sharex=True)

axs[0].plot(df.index, df['ingresos_totales'], marker='o', linestyle='-', color='tab:blue')
axs[0].set_title("Ingresos Totales (1990-2021)")
axs[0].set_ylabel("% del PIB")
axs[0].grid(True)

axs[1].plot(df.index, df['egresos_totales'], marker='s', linestyle='-', color='tab:red')
axs[1].set_title("Egresos Totales (1990-2021)")
axs[1].set_ylabel("% del PIB")
axs[1].grid(True)

axs[2].plot(df.index, df['resultado_fiscal_global'], marker='^', linestyle='-', color='tab:green')
axs[2].set_title("Resultado Fiscal Global (1990-2021)")
axs[2].set_xlabel("Año")
axs[2].set_ylabel("% del PIB")
axs[2].grid(True)

plt.xticks(df.index, rotation=45)
plt.tight_layout()
filename_combined = os.path.join(output_dir, "operaciones_empresas_publicas_combined.png")
fig.savefig(filename_combined, dpi=300)
plt.close(fig)
