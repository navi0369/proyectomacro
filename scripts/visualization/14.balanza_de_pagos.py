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
df = pd.read_sql("SELECT * FROM balanza_de_pagos", conn)
df.set_index('año', inplace=True)
df.index = df.index.astype(int)
conn.close()

# 2) Definir carpeta de salida para las imágenes
output_dir = "../../assets/imagenes/14.balanza_de_pagos"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
df

# %%
# Gráfica 1: Evolución de la Cuenta Corriente (I. CUENTA CORRIENTE)
plt.figure(figsize=(12,6))
plt.plot(df.index, df['current_account'], marker='o', linestyle='-', 
         color='tab:blue', linewidth=2, markersize=6, label='Cuenta Corriente')
plt.title("Evolución de la Cuenta Corriente", fontsize=16)
plt.xlabel("Año", fontsize=14)
plt.ylabel("Millones de USD", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.xticks(df.index, rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "cuenta_corriente.png"), dpi=300)
plt.close()

# Gráfica 2: Evolución de la Cuenta Capital (II. CUENTA CAPITAL)
plt.figure(figsize=(12,6))
plt.plot(df.index, df['capital_account'], marker='s', linestyle='-', 
         color='tab:green', linewidth=2, markersize=6, label='Cuenta Capital')
plt.title("Evolución de la Cuenta Capital", fontsize=16)
plt.xlabel("Año", fontsize=14)
plt.ylabel("Millones de USD", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.xticks(df.index, rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "cuenta_capital.png"), dpi=300)
plt.close()

# Gráfica 3: Evolución de Errores y Omisiones (III. ERRORES Y OMISIONES)
plt.figure(figsize=(12,6))
plt.plot(df.index, df['errors_omissions'], marker='^', linestyle='-', 
         color='tab:red', linewidth=2, markersize=6, label='Errores y Omisiones')
plt.title("Evolución de Errores y Omisiones", fontsize=16)
plt.xlabel("Año", fontsize=14)
plt.ylabel("Millones de USD", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.xticks(df.index, rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "errores_omisiones.png"), dpi=300)
plt.close()

# Gráfica 4: Evolución del BOP Balance (IV. SUPERÁVIT O DÉFICIT DE BdeP)
plt.figure(figsize=(12,6))
plt.plot(df.index, df['bop_balance'], marker='o', linestyle='-', 
         color='tab:purple', linewidth=2, markersize=6, label='BOP Balance')
plt.title("Evolución del BOP Balance", fontsize=16)
plt.xlabel("Año", fontsize=14)
plt.ylabel("Millones de USD", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.xticks(df.index, rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "bop_balance.png"), dpi=300)
plt.close()

# Gráfica 5: Evolución del Financiamiento (V. FINANCIAMIENTO)
plt.figure(figsize=(12,6))
plt.plot(df.index, df['financing'], marker='s', linestyle='-', 
         color='tab:orange', linewidth=2, markersize=6, label='Financiamiento')
plt.title("Evolución del Financiamiento", fontsize=16)
plt.xlabel("Año", fontsize=14)
plt.ylabel("Millones de USD", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.xticks(df.index, rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "financing.png"), dpi=300)
plt.close()

# Gráfica 6: Gráfica combinada de todos los indicadores
plt.figure(figsize=(12,6))
plt.plot(df.index, df['current_account'], marker='o', linestyle='-', color='tab:blue', linewidth=2, markersize=6, label='Cuenta Corriente')
plt.plot(df.index, df['capital_account'], marker='s', linestyle='-', color='tab:green', linewidth=2, markersize=6, label='Cuenta Capital')
plt.plot(df.index, df['errors_omissions'], marker='^', linestyle='-', color='tab:red', linewidth=2, markersize=6, label='Errores y Omisiones')
plt.plot(df.index, df['bop_balance'], marker='o', linestyle='-', color='tab:purple', linewidth=2, markersize=6, label='BOP Balance')
plt.plot(df.index, df['financing'], marker='s', linestyle='-', color='tab:orange', linewidth=2, markersize=6, label='Financiamiento')
plt.title("Evolución de la Balanza de Pagos", fontsize=16)
plt.xlabel("Año", fontsize=14)
plt.ylabel("Millones de USD", fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(df.index, rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "balanza_de_pagos_combinada.png"), dpi=300)
plt.close()
