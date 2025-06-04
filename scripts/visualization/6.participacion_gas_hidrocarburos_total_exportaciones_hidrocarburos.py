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
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Conectar a la base de datos y cargar los datos
conn = sqlite3.connect("../../db/proyectomacro.db")
df = pd.read_sql("SELECT * FROM participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos", conn)
conn.close()
# Directorio de salida
output_dir = "../../assets/imagenes/6.participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
df.head()


# %%
# 1) Gráfica de líneas: evolución de exportación de gas y otros hidrocarburos
plt.figure(figsize=(8,6))
sns.lineplot(data=df, x="año", y="exportacion_gas", marker="o", label="Exportación Gas")
sns.lineplot(data=df, x="año", y="otros_hidrocarburos", marker="o", label="Otros Hidrocarburos")
plt.title("Evolución de Exportaciones de Gas y Otros Hidrocarburos")
plt.xlabel("Año")
plt.ylabel("Porcentaje")
plt.legend()
plt.tight_layout()
plt.xticks(df["año"][::2],rotation=45)
plt.grid()
plt.savefig(os.path.join(output_dir, "6.1_evolucion_exportaciones.png"))
plt.close()

# 2) Gráfica de barras apiladas: participación de gas vs. otros hidrocarburos
plt.figure(figsize=(8,6))
# Para usar barras apiladas con seaborn, creamos dos barplots con bottom
sns.barplot(data=df, x="año", y="exportacion_gas", color="skyblue", label="Exportación Gas")
sns.barplot(data=df, x="año", y="otros_hidrocarburos",
            bottom=df["exportacion_gas"], color="lightgreen", label="Otros Hidrocarburos")
plt.title("Participación de Gas y Otros Hidrocarburos (Barras Apiladas)")
plt.xlabel("Año")
plt.ylabel("Porcentaje")
plt.legend()
plt.tight_layout()
plt.xticks(rotation=45)
plt.savefig(os.path.join(output_dir, "6.2_barras_apiladas.png"))
plt.close()

