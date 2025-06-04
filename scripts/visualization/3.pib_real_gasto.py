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

# Conectar a la base de datos y cargar los datos
conn = sqlite3.connect("../../db/proyectomacro.db")
df = pd.read_sql_query("SELECT * FROM pib_real_gasto", conn)
conn.close()

# Asegurarse que la columna 'año' sea numérica
df['año'] = df['año'].astype(int)

# Definir componentes y columna del PIB
componentes = [
    'gastos_consumo',
    'formacion_capital',
    'exportacion_bienes_servicios',
    'importacion_bienes',
    'consumo_privado',
    'consumo_publico'
]
pib_col = 'pib_real_base_1990'
df[pib_col] = df[pib_col] / 1_000_000 
# Definir directorio de salida y crearlo si no existe
output_dir = "../../assets/imagenes/3.pib_real_gasto/serie_completa"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 1. Gráfico del PIB
plt.figure(figsize=(10, 6))
plt.plot(df['año'], df[pib_col], color='black', linewidth=2)
plt.title('PIB Real Base 1990')
plt.xlabel('Año')
plt.ylabel('Millones de Bolivianos')
plt.grid(True)
plt.tight_layout()
plt.xticks(df['año'][::2], rotation=45)
plt.savefig(os.path.join(output_dir, '3.pib_real_base_1990.png'), bbox_inches='tight', dpi=300)
plt.close()

# 2. Gráficos separados para cada componente
for i, comp in enumerate(componentes):
    plt.figure(figsize=(10, 6))
    plt.plot(df['año'], df[comp], linewidth=2)
    # Convertir el nombre del componente a un título legible
    titulo = comp.replace('_', ' ').title()
    plt.title(titulo)
    plt.xlabel('Año')
    plt.ylabel('Millones de bolivianos')
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(df['año'][::2], rotation=45)
    filename = f"3.{i+1}{comp}.png"
    plt.savefig(os.path.join(output_dir, filename), bbox_inches='tight', dpi=300)
    plt.close()

# %%
# Definir periodos: (start_year, end_year, folder_name)
periods = [
    (1952, 1982, "periodo_1952-1982"),
    (1983, 2005, "periodo_1982-2006"),
    (2006, 2025, "periodo_2006-2025")
]

# Lista de componentes del PIB que se quieren graficar
componentes = [
    'gastos_consumo',
    'formacion_capital',
    'exportacion_bienes_servicios',
    'importacion_bienes',
    'consumo_privado',
    'consumo_publico'
]

def plot_component_period(df, component, start, end, period_folder, output_folder):
    """
    Genera y guarda la gráfica del componente del PIB entre 'start' y 'end'.
    
    Parámetros:
      - df: DataFrame de PIB (sin cambiar la variable original).
      - component: Nombre de la columna a graficar.
      - start, end: Años que delimitan el periodo.
      - period_folder: Nombre de la carpeta (ej. "periodo_1952-1982") para el título.
      - output_folder: Carpeta donde guardar la imagen.
    """
    # Filtrar DataFrame por el periodo
    df_period = df[(df['año'] >= start) & (df['año'] <= end)]
    
    # Calcular estadísticas descriptivas (media y std)
    media = df_period[component].mean()
    std_dev = df_period[component].std()
    
    plt.figure(figsize=(10, 6))
    plt.plot(df_period['año'], df_period[component], linewidth=2, marker='o')
    # Formatear el título (convertir snake_case a título legible)
    titulo = component.replace('_', ' ').title() + f" ({period_folder})"
    plt.title(titulo, fontsize=14)
    plt.xlabel("Año", fontsize=12)
    plt.ylabel("Millones de bolivianos", fontsize=12)
    plt.grid(True)
    plt.xticks(df_period['año'][::2], rotation=45)
    
    # Añadir anotación con estadísticas en la esquina superior central
    if not df_period.empty:
        x_ref = (start + end) / 2
        y_ref = df_period[component].max() * 0.8
        plt.text(x_ref, y_ref,
                 f"Media: {media:.2f}\nStd: {std_dev:.2f}",
                 fontsize=10,
                 bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
    
    # Guardar la gráfica
    filename = f"{component}_{period_folder}.png"
    plt.savefig(os.path.join(output_folder, filename), bbox_inches="tight", dpi=300)
    plt.close()

# Generar las gráficas por periodos para cada componente del PIB
# Se asume que df_pib ya está cargado y que la columna 'año' es numérica

for start, end, folder in periods:
    # Directorio de salida para el periodo actual
    output_folder = os.path.join("../../assets/imagenes/3.pib_real_gasto", folder)
    os.makedirs(output_folder, exist_ok=True)
    
    for component in componentes:
        plot_component_period(df, component, start, end, folder, output_folder)

