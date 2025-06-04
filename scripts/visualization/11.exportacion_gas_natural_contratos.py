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
conn = sqlite3.connect("../../db/proyectomacro.db")
df = pd.read_sql("SELECT * FROM exportacion_gas_natural_contratos", conn)
df.set_index('año',inplace=True)
df.index = df.index.astype(int)
conn.close()
output_dir = "../../assets/imagenes/11.exportacion_gas_natural_contratos"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
df

# %%
# 2) Evolución por Destino (Argentina vs. Brasil)
# Agrupamos por (año, destino), sumamos monto y reestructuramos con unstack()
df_destino = df.groupby(['año', 'destino'])['monto'].sum().unstack(fill_value=0)

plt.figure(figsize=(10,6))
for column in df_destino.columns:
    plt.plot(df_destino.index, df_destino[column], marker='o', linewidth=2, label=column)
plt.title("Evolución de Exportaciones de Gas Natural por Destino", fontsize=14)
plt.xlabel("Año", fontsize=12)
plt.ylabel("Monto (Millones de USD)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(df_destino.index, rotation=45)
plt.legend(title="Destino", fontsize=10)
plt.tight_layout()
plt.savefig(f"{output_dir}/11.2_evolucion_por_destino.png", dpi=300)
plt.show()
plt.close()

# Sumar el monto total por contrato y ordenar
contratos_totales = df.groupby('contrato')['monto'].sum().sort_values(ascending=False)

# Tomar los 3 contratos principales
top_contratos = contratos_totales.head(3).index.tolist()

# Nueva columna: si el contrato está en el top 3, se mantiene; si no, se asigna "Otros"
df['contrato_mod'] = df['contrato'].apply(lambda x: x if x in top_contratos else 'Otros')

# Agrupar por año y contrato_mod, luego reestructurar
df_line = df.groupby(['año', 'contrato_mod'])['monto'].sum().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(10,6))
df_line.plot(ax=ax, marker='o', linewidth=2.5, markersize=4)

ax.set_title("Evolución de Exportaciones por Contrato (Top 3 + Otros)", fontsize=14)
ax.set_xlabel("Año", fontsize=12)
ax.set_ylabel("Monto (Millones de USD)", fontsize=12)
ax.grid(True, linestyle='--', alpha=0.7)

ax.set_xticks(df_line.index)
ax.set_xticklabels(df_line.index, rotation=45, fontsize=10)

ax.legend(title="Contrato", fontsize=9, title_fontsize=10)
plt.tight_layout()
plt.savefig(f"{output_dir}/11.3_distribucion_por_contrato_multiline.png", dpi=300)
plt.show()
plt.close()



