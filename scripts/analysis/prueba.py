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
import matplotlib.pyplot as plt
import sqlite3
import os
import seaborn as sns

# --- Estilo profesional ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'grid.linestyle': '--',
    'lines.linewidth': 2,
    'figure.dpi': 150,
    'savefig.bbox': 'tight'
})

# --- Conexión y carga de datos ---
conn = sqlite3.connect('../../db/proyectomacro.db')
tablas = {
    "pib": "pib_real_gasto",
    "minerales": "exportaciones_minerales_totales",
    "balanza": "balanza_comercial",
    "reservas": "Reservas_oro_divisas",
    "precios": "precio_oficial_minerales"
}
df = {k: pd.read_sql_query(f"SELECT * FROM {v}", conn).set_index('año')
      for k, v in tablas.items()}
conn.close()

# --- Procesamiento previo ---
df["pib"] /= 1000
valor_cols = ['estaño_valor', 'plomo_valor', 'zinc_valor', 'plata_valor', 
              'wolfram_valor', 'cobre_valor', 'antimonio_valor', 'oro_valor']
df["minerales"]["valor_total"] = df["minerales"][valor_cols].sum(axis=1) / 1000

# --- Definición de periodos y creación de carpetas ---
periodos = {
    "pre": (1952, 1956),
    "post": (1956, 1982)
}

base_path = "../../assets/tesis/intervensionismo_estatal"
os.makedirs(base_path, exist_ok=True)
for nombre, (inicio, fin) in periodos.items():
    os.makedirs(os.path.join(base_path, f"{inicio}-{fin}"), exist_ok=True)

# --- Funciones auxiliares ---
def add_text_inicio_fin(x, y, offset_first=(0.5, 0), offset_last=(-0.5, 0), color='black'):
    # Anotación del primer punto
    plt.text(
        x[0] + offset_first[0],
        y.iloc[0] + offset_first[1],
        f'{y.iloc[0]:.2f}',
        fontsize=12,
        va='bottom',
        ha='right',
        color=color
    )
    # Anotación del último punto
    plt.text(
        x[-1] + offset_last[0],
        y.iloc[-1] + offset_last[1],
        f'{y.iloc[-1]:.2f}',
        fontsize=12,
        va='bottom',
        ha='left',
        color=color
    )


def graficar_serie(x, y, titulo, ylabel, nombre_archivo, carpeta, inicio):
    plt.figure()
    plt.plot(x, y)
    plt.title(titulo, fontweight='bold')
    plt.xlabel('Año')
    plt.ylabel(ylabel)
    plt.grid(True)
    if inicio==1952:
        plt.xticks(x, rotation=45)
    else:
        plt.xticks(x[::2], rotation=45)

    if titulo=="PIB Real (Base 1990)" and inicio==1956:
        add_text_inicio_fin(x, y, offset_first=(1,500))
    else:   
        add_text_inicio_fin(x, y)
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta, nombre_archivo))
    plt.close()

def grafico_import_export(df_balanza, carpeta, inicio):
    x = df_balanza.index
    plt.figure()
    plt.plot(x, df_balanza['importaciones'], label='Importaciones')
    plt.plot(x, df_balanza['exportaciones'], label='Exportaciones', color='darkorange')
    if inicio==1952:
        add_text_inicio_fin(x, df_balanza['importaciones'], color='#1f77b4')
        add_text_inicio_fin(x, df_balanza['exportaciones'], color='darkorange')
    else:
        add_text_inicio_fin(x, df_balanza['importaciones'], color='#1f77b4',offset_first=(0,-20),offset_last=(0,-20))
        add_text_inicio_fin(x, df_balanza['exportaciones'], color='darkorange', offset_last=(0,20))
    plt.title('Importaciones y Exportaciones - Período Post Crisis', fontweight='bold')
    plt.xlabel('Año')
    plt.ylabel('Millones de USD')
    plt.grid(True)
    plt.legend()
    print(inicio)
    if inicio==1952:
        plt.xticks(x, rotation=45)
        print('tarmeno')
    else:
        plt.xticks(x[::2], rotation=45)
        print('tarmeno 2')
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta, "Importaciones_Exportaciones.png"))
    plt.close()
# Nueva función para generar gráficos de barras (usada para Saldo Comercial)
def graficar_barra(x, y, titulo, ylabel, nombre_archivo, carpeta, inicio):
    plt.figure(figsize=(10,6))
    # Colores condicionales: azul para Crisis, rojo para Post Crisis
    colors = ['red' if year < 1956 else '#1f77b4' for year in x]
    plt.bar(x, y, color=colors)
    add_text_inicio_fin(x, y,offset_first=(0,0),offset_last=(0,0))
    plt.title(titulo, fontweight='bold')
    plt.xlabel('Año')
    plt.ylabel(ylabel)
    plt.grid(True, axis='y', linestyle='--')
    plt.xticks(x, rotation=45)
    
    # Agregar anotaciones para cada barra (puedes ajustar el offset vertical)
    
    
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta, nombre_archivo))
    plt.close()
# --- Generación de gráficos por período ---
for nombre, (inicio, fin) in periodos.items():
    carpeta = os.path.join(base_path, f"{inicio}-{fin}")
    df_p = df["pib"].loc[inicio:fin]
    df_r = df["reservas"].loc[inicio:fin]
    df_m = df["minerales"].loc[inicio:fin]
    df_b = df["balanza"].loc[inicio:fin]

    graficar_serie(df_p.index, df_p["pib_real_base_1990"],
                   "PIB Real (Base 1990)", "Millones de bolivianos 1990", "PIB_Real.png", carpeta,inicio)

    graficar_serie(df_r.index, df_r["reservas_totales"],
                   "Reservas Internacionales", "Millones USD", "Reservas.png", carpeta,inicio)

    graficar_serie(df_m.index, df_m["valor_total"],
                   "Exportaciones Minerales", "Millones USD", "Minerales.png", carpeta, inicio)

    grafico_import_export(df_b, carpeta, inicio)

     # Ahora usar la función de barras para Saldo Comercial
    graficar_barra(df_b.index, df_b["saldo_comercial"],
                   "Saldo Comercial", "Millones USD", "Saldo_Comercial.png", carpeta, inicio)

