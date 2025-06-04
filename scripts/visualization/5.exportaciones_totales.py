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
df = pd.read_sql("SELECT * FROM exportaciones_totales", conn)
conn.close()
# Directorio de salida
output_dir = "../../assets/imagenes/5.exportaciones_totales/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# %%
# Ajustes generales para las gráficas
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (8, 5)

# 1. Evolución del valor oficial total
plt.figure()
sns.lineplot(data=df, x="año", y="total_valor_oficial", marker="o")
plt.title("Evolución del Valor Oficial Total")
plt.xlabel("Año")
plt.ylabel("Millones de USD")
plt.savefig(os.path.join(output_dir, "5.1_evolucion_valor_total.png"))
plt.close()

# 2. Comparación de exportaciones tradicionales vs no tradicionales
plt.figure()
sns.lineplot(data=df, x="año", y="productos_tradicionales", marker="o", label="Tradicionales")
sns.lineplot(data=df, x="año", y="productos_no_tradicionales", marker="o", label="No Tradicionales")
plt.title("Exportaciones Tradicionales vs No Tradicionales")
plt.xlabel("Año")
plt.ylabel("Millones de USD")
plt.legend()
plt.savefig(os.path.join(output_dir, "5.2_exportaciones_tradicionales_vs_no_tradicionales.png"))
plt.close()

# 3. Gráfica de barras apiladas (stacked) de tradicionales y no tradicionales
df.plot(
    x="año",
    y=["productos_tradicionales", "productos_no_tradicionales"],
    kind="bar",
    stacked=True,
    title="Exportaciones (Tradicionales y No Tradicionales)",
    figsize=(8, 5)
)
plt.xlabel("Año")
plt.ylabel("Millones de USD")
plt.legend(["Tradicionales", "No Tradicionales"])
plt.savefig(os.path.join(output_dir, "5.3_exportaciones_stacked_bar.png"))
plt.close()

# 4. Porcentaje de participación de cada categoría en el total
df["pct_tradicional"] = df["productos_tradicionales"] / df["total_valor_oficial"] * 100
df["pct_no_tradicional"] = df["productos_no_tradicionales"] / df["total_valor_oficial"] * 100

plt.figure()
sns.lineplot(data=df, x="año", y="pct_tradicional", marker="o", label="% Tradicional")
sns.lineplot(data=df, x="año", y="pct_no_tradicional", marker="o", label="% No Tradicional")
plt.title("Porcentaje de Exportaciones Tradicionales vs No Tradicionales")
plt.xlabel("Año")
plt.ylabel("Porcentaje (%)")
plt.legend()
plt.savefig(os.path.join(output_dir, "5.4_porcentaje_exportaciones.png"))
plt.close()

# 5. Distribución y relaciones entre variables (pairplot)
sns.pairplot(df[["productos_tradicionales", "productos_no_tradicionales", "total_valor_oficial"]], diag_kind="kde")
plt.suptitle("Distribución y Relaciones entre Variables", y=1.02)
plt.savefig(os.path.join(output_dir, "5.5_distribucion_pairplot.png"))
plt.close()
