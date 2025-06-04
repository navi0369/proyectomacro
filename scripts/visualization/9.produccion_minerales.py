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
df = pd.read_sql("SELECT * FROM produccion_minerales", conn)
conn.close()
df.head()

# %%
# Definir directorio de salida
output_dir = "../../assets/imagenes/9.produccion_minerales"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Asegurarse de que 'año' es int y establecerlo como índice
df['año'] = df['año'].astype(int)
df = df.set_index('año')

# Definir periodos
df_periodo1 = df.loc[:1985]
df_periodo2 = df.loc[1986:2006]
df_periodo3 = df.loc[2006:]

# Seleccionar mineral
mineral = 'zinc'

# Calcular estadísticas
media_p1, std_p1 = df_periodo1[mineral].mean(), df_periodo1[mineral].std()
media_p2, std_p2 = df_periodo2[mineral].mean(), df_periodo2[mineral].std()
media_p3, std_p3 = df_periodo3[mineral].mean(), df_periodo3[mineral].std()

# Crear la figura
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], linewidth=2)
ax.set_title("Producción de Zinc", fontsize=14)
ax.set_xlabel("Año", fontsize=12)
ax.set_ylabel("Toneladas Finas", fontsize=12)
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)

# Anotaciones (ajustar posición según la escala de datos)
ax.text(1990, df[mineral].max()*0.8, f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
ax.text(2010, 200000, f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

# Guardar la imagen
plt.savefig(os.path.join(output_dir, "9.1.zinc.png"), bbox_inches="tight", dpi=300)
plt.close()

# %%
mineral = 'estaño'

media_p2, std_p2 = df_periodo2[mineral].mean(), df_periodo2[mineral].std()
media_p3, std_p3 = df_periodo3[mineral].mean(), df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], linewidth=2)
ax.set_title("Producción de Estaño", fontsize=14)
ax.set_xlabel("Año", fontsize=12)
ax.set_ylabel("Toneladas Finas", fontsize=12)
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)


ax.text(1990, 9000, f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
ax.text(2010, 9000, f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.savefig(os.path.join(output_dir, "9.2.estaño.png"), bbox_inches="tight", dpi=300)
plt.close()

# %%
mineral = 'oro'


media_p2, std_p2 = df_periodo2[mineral].mean(), df_periodo2[mineral].std()
media_p3, std_p3 = df_periodo3[mineral].mean(), df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], linewidth=2)
ax.set_title("Producción de Oro", fontsize=14)
ax.set_xlabel("Año", fontsize=12)
ax.set_ylabel("Toneladas Finas", fontsize=12)
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)

ax.text(1990, df[mineral].max()*0.8, f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
ax.text(2010, df[mineral].max()*0.8, f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.savefig(os.path.join(output_dir, "9.3.oro.png"), bbox_inches="tight", dpi=300)
plt.close()


# %%
mineral = 'plata'

media_p2, std_p2 = df_periodo2[mineral].mean(), df_periodo2[mineral].std()
media_p3, std_p3 = df_periodo3[mineral].mean(), df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], linewidth=2)
ax.set_title("Producción de Plata", fontsize=14)
ax.set_xlabel("Año", fontsize=12)
ax.set_ylabel("Toneladas Finas", fontsize=12)
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)


ax.text(1990, df[mineral].max()*0.8, f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
ax.text(2010, 200, f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.savefig(os.path.join(output_dir, "9.4.plata.png"), bbox_inches="tight", dpi=300)
plt.close()


# %%
mineral = 'antimonio'

media_p2, std_p2 = df_periodo2[mineral].mean(), df_periodo2[mineral].std()
media_p3, std_p3 = df_periodo3[mineral].mean(), df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], linewidth=2)
ax.set_title("Producción de Antimonio", fontsize=14)
ax.set_xlabel("Año", fontsize=12)
ax.set_ylabel("Toneladas Finas", fontsize=12)
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)

ax.text(1990, df[mineral].max()*0.8, f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
ax.text(2010, df[mineral].max()*0.8, f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.savefig(os.path.join(output_dir, "9.5.antimonio.png"), bbox_inches="tight", dpi=300)
plt.close()

# %%
mineral = 'plomo'

media_p2, std_p2 = df_periodo2[mineral].mean(), df_periodo2[mineral].std()
media_p3, std_p3 = df_periodo3[mineral].mean(), df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], linewidth=2)
ax.set_title("Producción de Plomo", fontsize=14)
ax.set_xlabel("Año", fontsize=12)
ax.set_ylabel("Toneladas Finas", fontsize=12)
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)


ax.text(1990, df[mineral].max()*0.8, f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
ax.text(2010, 20000, f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.savefig(os.path.join(output_dir, "9.6.plomo.png"), bbox_inches="tight", dpi=300)
plt.close()

# %%
mineral = 'wolfram'


media_p2, std_p2 = df_periodo2[mineral].mean(), df_periodo2[mineral].std()
media_p3, std_p3 = df_periodo3[mineral].mean(), df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], linewidth=2)
ax.set_title("Producción de Wólfram", fontsize=14)
ax.set_xlabel("Año", fontsize=12)
ax.set_ylabel("Toneladas Finas", fontsize=12)
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)


ax.text(1990, df[mineral].max()*0.8, f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
ax.text(2010, 600, f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.savefig(os.path.join(output_dir, "9.7.wolfram.png"), bbox_inches="tight", dpi=300)
plt.close()

# %%
mineral = 'cobre'


media_p2, std_p2 = df_periodo2[mineral].mean(), df_periodo2[mineral].std()
media_p3, std_p3 = df_periodo3[mineral].mean(), df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], linewidth=2)
ax.set_title("Producción de Cobre", fontsize=14)
ax.set_xlabel("Año", fontsize=12)
ax.set_ylabel("Toneladas Finas", fontsize=12)
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)


ax.text(1990, df[mineral].max()*0.8, f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
ax.text(2010, 0, f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.savefig(os.path.join(output_dir, "9.8.cobre.png"), bbox_inches="tight", dpi=300)
plt.close()
