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
import numpy as np
import matplotlib.pyplot as plt

# Años y medias anuales (en el mismo orden)
years = np.array([
    1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011,
    2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019,
    2020, 2021, 2022, 2023
])

means = np.array([
    22.113333, 20.610000, 14.446667, 19.260833, 30.300833,
    25.947500, 26.115000, 31.120833, 41.443333, 56.492500,
    66.018333, 72.318333, 99.571667, 61.654167, 79.395000,
    94.874167, 94.110833, 97.905833, 93.258333, 48.688333,
    43.144167, 50.884167, 64.938333, 56.984167, 39.227500,
    67.963333, 94.439167, 77.687500
])
annotate_up = [2005, 2008,2020, 2022,2023]
annotate_down = [1996, 2009, 2013, 2014, 2016]
# 1) Crear la figura con tamaño 10x6
plt.figure(figsize=(10, 6))

# 2) Trazar la línea del precio WTI
plt.plot(
    years, means,
    marker='o', color='tab:blue', linewidth=2, markersize=6,
    label='WTI (Media Anual)'
)

# 3) Título y etiquetas
plt.title("Evolución del Precio Internacional del Petróleo (WTI) (1996-2023)", fontsize=14)
plt.xlabel("Año", fontsize=12)
plt.ylabel("USD por barril", fontsize=12)
plt.xticks(years,rotation=45)
# 4) Cuadrícula
plt.grid(True, linestyle='--', alpha=0.7)

# 5) Leyenda
plt.legend()
def annotate_point(year_list, vertical_align):
    for y in year_list:
        idx = np.where(years == y)[0]
        if len(idx) > 0:
            i = idx[0]
            x_val = years[i]
            y_val = means[i]
            offset = 5 if vertical_align == 'bottom' else -5
            plt.annotate(
                text=f"{y_val:.2f}",
                xy=(x_val, y_val),
                xytext=(0, offset),
                textcoords="offset points",
                ha='center',
                va=vertical_align,
                fontsize=10,
                fontweight='bold',
                color='red' if vertical_align == 'bottom' else 'blue',
                arrowprops=None
            )

# Anotaciones "arriba" (va='bottom')
annotate_point(annotate_up, 'bottom')

# Anotaciones "abajo" (va='top')
annotate_point(annotate_down, 'top')
# 6) Ajustar la distribución
plt.tight_layout()


# 7) Mostrar la gráfica
plt.show()
