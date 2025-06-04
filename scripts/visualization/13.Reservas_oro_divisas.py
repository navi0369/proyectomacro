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
import os
# Conectar a la base de datos y cargar los datos
# 1) Conectar a la base de datos y cargar los datos
conn = sqlite3.connect("../../db/proyectomacro.db")
df = pd.read_sql("SELECT * FROM reservas_oro_divisas", conn)
df.set_index('año', inplace=True)
df.index = df.index.astype(int)
df['reservas_totales']=df['reservas_totales']/1000000000
conn.close()

# 2) Definir carpeta de salida para las imágenes
output_dir = "../../assets/imagenes/13.Reservas_oro_divisas"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
df

# %%
# 4) Graficar la evolución de las reservas
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['reservas_totales'], marker='o', color='tab:blue', linewidth=2, markersize=6, label='Reservas Totales')
plt.title("Evolución de las Reservas de Oro y Divisas", fontsize=14)
plt.xlabel("Año", fontsize=12)
plt.ylabel("Miles de millones de USD", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

# 5) Guardar la gráfica
output_file = os.path.join(output_dir, "13.1reservas_oro_divisas_evolucion.png")
plt.savefig(output_file, dpi=300)
plt.show()
plt.close()
