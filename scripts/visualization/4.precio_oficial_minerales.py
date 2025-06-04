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
df = pd.read_sql("SELECT * FROM precio_oficial_minerales where año>1955", conn)
conn.close()
df

# %%
#ZINC
# Definir directorio de salida
output_dir = "../../assets/imagenes/4.precio_oficial_minerales"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# Convertir 'año' en índice
df['año'] = df['año'].astype(int)
df = df.set_index('año')

# Definir los periodos
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
ax.plot(df.index, df[mineral], marker='o', linewidth=2)
ax.set_title("Zinc")
ax.set_xlabel("Año")
ax.set_ylabel("Precio (USD)")
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)

# Definir posiciones de las anotaciones
ax.text(1960, 1.2, f"Periodo 1 (1952-1985)\nMedia: {media_p1:.2f}\nStd: {std_p1:.2f}", fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
ax.text(1980, 1.2, f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}", fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
ax.text(2008, 0.2, f"Periodo 3 (2006-2023)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}", fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

# Guardar la imagen
plt.savefig(os.path.join(output_dir, "4.1.zinc.png"), bbox_inches="tight", dpi=300)
plt.close()


# %%
#ESTAÑO
# Seleccionar mineral
mineral = 'estaño'

# Calcular estadísticas
media_p1, std_p1 = df_periodo1[mineral].mean(), df_periodo1[mineral].std()
media_p2, std_p2 = df_periodo2[mineral].mean(), df_periodo2[mineral].std()
media_p3, std_p3 = df_periodo3[mineral].mean(), df_periodo3[mineral].std()

# Crear la figura
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], marker='o', linewidth=2)
ax.set_title("Estaño")
ax.set_xlabel("Año")
ax.set_ylabel("Precio (USD)")
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)

# Definir posiciones de las anotaciones
ax.text(1958, 10, f"Periodo 1 (1952-1985)\nMedia: {media_p1:.2f}\nStd: {std_p1:.2f}", fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
ax.text(1986, 10, f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}", fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
ax.text(2008, 2, f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}", fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

# Guardar la imagen
plt.savefig(os.path.join(output_dir, "4.2.estano.png"), bbox_inches="tight", dpi=300)
plt.close()


# %%
#ORO
# Seleccionar mineral
mineral = 'oro'

# Calcular estadísticas
media_p1, std_p1 = df_periodo1[mineral].mean(), df_periodo1[mineral].std()
media_p2, std_p2 = df_periodo2[mineral].mean(), df_periodo2[mineral].std()
media_p3, std_p3 = df_periodo3[mineral].mean(), df_periodo3[mineral].std()

# Crear la figura
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], marker='o', linewidth=2)
ax.set_title("Oro")
ax.set_xlabel("Año")
ax.set_ylabel("Precio (USD)")
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)

# Definir posiciones de las anotaciones
ax.text(1960, 1200, f"Periodo 1 (≤1985)\nMedia: {media_p1:.2f}\nStd: {std_p1:.2f}", fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
ax.text(1980, 1200, f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}", fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))
ax.text(2008, 500, f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}", fontsize=10, bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

# Guardar la imagen
plt.savefig(os.path.join(output_dir, "4.3.oro.png"), bbox_inches="tight", dpi=300)
plt.close()


# %%
#PLATA
mineral = 'plata'

# Calcular estadísticas para cada periodo
media_p1 = df_periodo1[mineral].mean()
std_p1   = df_periodo1[mineral].std()

media_p2 = df_periodo2[mineral].mean()
std_p2   = df_periodo2[mineral].std()

media_p3 = df_periodo3[mineral].mean()
std_p3   = df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], marker='o', linewidth=2)
ax.set_title("Plata")
ax.set_xlabel("Año")
ax.set_ylabel("Precio")
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)

# Ajusta estas posiciones según la escala de tu serie
ax.text(1965, 30,
        f"Periodo 1 (≤1985)\nMedia: {media_p1:.2f}\nStd: {std_p1:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(1988, 30,
        f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(2008, 5,
        f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "4.4.plata.png"), bbox_inches='tight', dpi=300)
plt.close()


# %%
#ANTIMONIO
mineral = 'antimonio'

media_p1 = df_periodo1[mineral].mean()
std_p1   = df_periodo1[mineral].std()

media_p2 = df_periodo2[mineral].mean()
std_p2   = df_periodo2[mineral].std()

media_p3 = df_periodo3[mineral].mean()
std_p3   = df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], marker='o', linewidth=2)
ax.set_title("Antimonio")
ax.set_xlabel("Año")
ax.set_ylabel("Precio")
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)

ax.text(1965, 10000,
        f"Periodo 1 (≤1985)\nMedia: {media_p1:.2f}\nStd: {std_p1:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(1986, 10000,
        f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(2010, 20,
        f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "4.5.antimonio.png"), bbox_inches='tight', dpi=300)
plt.close()


# %%
#PLOMO
mineral = 'plomo'

media_p1 = df_periodo1[mineral].mean()
std_p1   = df_periodo1[mineral].std()

media_p2 = df_periodo2[mineral].mean()
std_p2   = df_periodo2[mineral].std()

media_p3 = df_periodo3[mineral].mean()
std_p3   = df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], marker='o', linewidth=2)
ax.set_title("Plomo")
ax.set_xlabel("Año")
ax.set_ylabel("Precio (USD)")
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)

ax.text(1965, 0.8,
        f"Periodo 1 (≤1985)\nMedia: {media_p1:.2f}\nStd: {std_p1:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(1985, 0.8,
        f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(2010, 0.5,
        f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "4.6.plomo.png"), bbox_inches='tight', dpi=300)
plt.close()


# %%
#WOLFRAM
mineral = 'wolfram'

media_p1 = df_periodo1[mineral].mean()
std_p1   = df_periodo1[mineral].std()

media_p2 = df_periodo2[mineral].mean()
std_p2   = df_periodo2[mineral].std()

media_p3 = df_periodo3[mineral].mean()
std_p3   = df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], marker='o', linewidth=2)
ax.set_title("Wolfram")
ax.set_xlabel("Año")
ax.set_ylabel("Precio")
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)

ax.text(1962, 150,
        f"Periodo 1 (≤1985)\nMedia: {media_p1:.2f}\nStd: {std_p1:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(1990, 150,
        f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(2012, 75,
        f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "4.7.wolfram.png"), bbox_inches='tight', dpi=300)
plt.close()


# %%
#COBRE
mineral = 'cobre'

media_p1 = df_periodo1[mineral].mean()
std_p1   = df_periodo1[mineral].std()

media_p2 = df_periodo2[mineral].mean()
std_p2   = df_periodo2[mineral].std()

media_p3 = df_periodo3[mineral].mean()
std_p3   = df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], marker='o', linewidth=2)
ax.set_title("Cobre")
ax.set_xlabel("Año")
ax.set_ylabel("Precio")
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)
 
ax.text(1965, 2.5,
        f"Periodo 1 (≤1985)\nMedia: {media_p1:.2f}\nStd: {std_p1:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(1985, 2.5,
        f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(2012, 1,
        f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "4.8.cobre.png"), bbox_inches='tight', dpi=300)
plt.close()


# %%
#BISMUTO
mineral = 'bismuto'

media_p1 = df_periodo1[mineral].mean()
std_p1   = df_periodo1[mineral].std()

media_p2 = df_periodo2[mineral].mean()
std_p2   = df_periodo2[mineral].std()

media_p3 = df_periodo3[mineral].mean()
std_p3   = df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], marker='o', linewidth=2)
ax.set_title("Bismuto")
ax.set_xlabel("Año")
ax.set_ylabel("Precio")
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)

ax.text(1965, 11,
        f"Periodo 1 (≤1985)\nMedia: {media_p1:.2f}\nStd: {std_p1:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(1985, 11,
        f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(2012, 3,
        f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "4.9.bismuto.png"), bbox_inches='tight', dpi=300)
plt.close()


# %%
#CADMIO
mineral = 'cadmio'

media_p1 = df_periodo1[mineral].mean()
std_p1   = df_periodo1[mineral].std()

media_p2 = df_periodo2[mineral].mean()
std_p2   = df_periodo2[mineral].std()

media_p3 = df_periodo3[mineral].mean()
std_p3   = df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], marker='o', linewidth=2)
ax.set_title("Cadmio")
ax.set_xlabel("Año")
ax.set_ylabel("Precio")
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)

ax.text(1965, 6,
        f"Periodo 1 (≤1985)\nMedia: {media_p1:.2f}\nStd: {std_p1:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(1995, 6,
        f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(2015, 6,
        f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "4.10.cadmio.png"), bbox_inches='tight', dpi=300)
plt.close()


# %%
#MANGANESO
mineral = 'manganeso'

media_p1 = df_periodo1[mineral].mean()
std_p1   = df_periodo1[mineral].std()

media_p2 = df_periodo2[mineral].mean()
std_p2   = df_periodo2[mineral].std()

media_p3 = df_periodo3[mineral].mean()
std_p3   = df_periodo3[mineral].std()

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df.index, df[mineral], marker='o', linewidth=2)
ax.set_title("Manganeso")
ax.set_xlabel("Año")
ax.set_ylabel("Precio")
ax.grid(True)
ax.set_xticks(df.index[::2])
plt.xticks(rotation=45)

ax.text(1965, 5,
        f"Periodo 1 (≤1985)\nMedia: {media_p1:.2f}\nStd: {std_p1:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(1985, 5,
        f"Periodo 2 (1986-2006)\nMedia: {media_p2:.2f}\nStd: {std_p2:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

ax.text(2012, 10,
        f"Periodo 3 (≥2006)\nMedia: {media_p3:.2f}\nStd: {std_p3:.2f}",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "4.11.manganeso.png"), bbox_inches='tight', dpi=300)
plt.close()

