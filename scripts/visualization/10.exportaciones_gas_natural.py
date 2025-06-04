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
df = pd.read_sql("SELECT * FROM exportacion_gas_natural", conn)
df.set_index('año',inplace=True)
df.index = df.index.astype(int)
conn.close()
output_dir = "../../assets/imagenes/10.exportaciones_gas_natural"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# %%
plt.figure(figsize=(12,6))
plt.plot(df.index, df['monto'], marker='o', linestyle='-', color='tab:blue', linewidth=2, markersize=6)
plt.title("Evolución de Exportaciones de Gas Natural (Monto)", fontsize=16)
plt.xlabel("Año", fontsize=14)
plt.ylabel("Monto (Millones de USD)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.xticks(df.index, rotation=45)
plt.savefig(os.path.join(output_dir, "10.1_evolucion_del_monto.png"), bbox_inches="tight", dpi=300)
plt.close()

# %%
plt.figure(figsize=(12,6))
plt.plot(df.index, df['toneladas'], marker='s', linestyle='-', color='tab:green', linewidth=2, markersize=6)
plt.title("Evolución de Exportaciones de Gas Natural (Toneladas)", fontsize=16)
plt.xlabel("Año", fontsize=14)
plt.ylabel("Toneladas", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.xticks(df.index, rotation=45)
plt.savefig(os.path.join(output_dir, "10.2_evolucion_de_cantidades.png"), bbox_inches="tight", dpi=300)
plt.close()
plt.show()


# %%
fig, ax1 = plt.subplots(figsize=(12,6))

# Eje para el Monto
color = 'tab:blue'
ax1.set_xlabel("Año", fontsize=14)
ax1.set_ylabel("Monto (Millones de USD)", color=color, fontsize=14)
ax1.plot(df.index, df['monto'], marker='o', linestyle='-', color=color, linewidth=2, markersize=6, label="Monto")
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle='--', alpha=0.7)

# Eje para las Toneladas
ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel("Toneladas", color=color, fontsize=14)
ax2.plot(df.index, df['toneladas'], marker='s', linestyle='-', color=color, linewidth=2, markersize=6, label="Toneladas")
ax2.tick_params(axis='y', labelcolor=color)

fig.suptitle("Evolución de Exportaciones de Gas Natural", fontsize=16)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
ax1.set_xticks(df.index[::2])  # cada 2 años
ax1.set_xticklabels(df.index[::2], rotation=45, fontsize=11)
plt.savefig(os.path.join(output_dir, "10.3_evolucion_de_monto_y_cantidades.png"), bbox_inches="tight", dpi=300)
plt.show()
plt.close()

# %%
plt.figure(figsize=(12,6))
plt.plot(df.index, df['precio'], marker='o', linestyle='-', color='tab:red', linewidth=2, markersize=6)
plt.title("Evolución del Precio del Gas Natural", fontsize=16)
plt.xlabel("Año", fontsize=14)
plt.ylabel("Precio (USD/Tonelada)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(df.index[::2], rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "10.4_evolucion_de_precios.png"), bbox_inches="tight", dpi=300)
plt.close()
plt.show()

