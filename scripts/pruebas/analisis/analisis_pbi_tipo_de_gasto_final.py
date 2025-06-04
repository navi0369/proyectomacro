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

# %%
# Producto Interno Bruto (a precios de mercado)
pib = [
  15261228, 15303291, 14700534, 14106321, 14078014, 13842012, 13485735, 13817954,
  14219987, 14758943, 15443136, 16256453, 16524115, 17229578, 18033729, 18877396,
  19700704, 20676718, 21716623, 21809329, 22356265, 22732700, 23297736, 23929417,
  24928062, 26030240, 27278913, 28524027, 30277826, 31294253, 32585680, 34281469,
  36037460, 38486570, 40588156, 42559599, 44374306, 46235900, 48188730, 49256933,
  44952919, 47700159, 49420074, 50943184
]

# Gasto de Consumo Final de la Administración Pública
consumo_publico = [
  2353886, 2551142, 2476904, 2185867, 2269149, 2101232, 1804538, 1735759,
  1801118, 1816974, 1815415, 1876065, 1945335, 1994606, 2057084, 2193477,
  2250628, 2326252, 2414668, 2492184, 2543985, 2616812, 2707278, 2804003,
  2892281, 2989344, 3087197, 3203527, 3328817, 3455979, 3562033, 3820034,
  4006653, 4378880, 4673103, 5101507, 5181454, 5437311, 5717179, 5932046,
  5768129, 6078973, 6306651, 6457609
]

# Gasto de Consumo Final de los Hogares e ISFLSH
consumo_hogares = [
  10804472, 10849053, 10414387, 9937018, 9934989, 10330240, 10844192, 11181302,
  11280821, 11482159, 11869886, 12264368, 12700433, 13122712, 13507684, 13905760,
  14359906, 15139505, 15934817, 16375001, 16752142, 16964766, 17311639, 17637776,
  18151035, 18755349, 19518921, 20332797, 21447627, 22235429, 23119867, 24322888,
  25443090, 26951156, 28411942, 29889225, 30904698, 32366730, 33758922, 34999860,
  32250375, 33973031, 35115806, 36231082
]

# Variación de Existencias
variacion_existencias = [
  -45476, -19461, 59743, 70418, 488416, 785209, 27396, 221846,
  195150, -62340, -4101, 192895, 47434, -22412, -88669, -136030,
  34669, 152949, 168730, -40285, 28275, 179627, 191765, 94705,
  -266128, 313327, -197120, -278546, 90127, 143332, 137207, 291386,
  -355490, -108420, 82779, -277958, 280087, 707786, 318339, 758657,
  604771, 645539, -62376, 472748
]

# Formación Bruta de Capital Fijo
formacion_bruta_capital_fijo = [
  1963222, 1922221, 1395659, 1222858, 1313044, 1499459, 1560452, 1644120,
  1742300, 1706846, 1939425, 2309228, 2587870, 2655895, 2442941, 2780084,
  3106141, 3937439, 5087830, 4310603, 3927006, 3084701, 3655612, 3259138,
  3222710, 3437559, 3757082, 4232114, 5022365, 5167461, 5553149, 6870021,
  7043534, 7869530, 8649250, 9081229, 9391366, 10496845, 10835839, 10460754,
  7749528, 8672724, 9158089, 9681315
]

# Exportaciones de Bienes y Servicios
exportaciones = [
  2888765, 2926118, 2542159, 2590570, 2433439, 1977362, 2355681, 2381708,
  2541495, 3166949, 3517480, 3774038, 3816036, 4018461, 4625108, 5046839,
  5252178, 5141346, 5474630, 4773615, 5491595, 5951639, 6290480, 7055594,
  8228272, 8914207, 9924796, 10231390, 10453875, 9329492, 10248692, 10719430,
  12144641, 12641952, 14015558, 13186019, 12432525, 11814068, 12427220, 12201083,
  9907297, 11435209, 13160823, 12006646
]

# Importaciones de Bienes y Servicios (se restan)
importaciones = [
  2703641, 2925782, 2188318, 1900411, 2361023, 2851490, 3106524, 3346783,
  3340896, 3351646, 3694970, 4160141, 4572994, 4539684, 4510420, 4912734,
  5302818, 6020772, 7364052, 6101790, 6386738, 6064846, 6859038, 6921800,
  7300109, 8379546, 8811963, 9197256, 10064984, 9037440, 10035269, 11742291,
  12244967, 13246528, 15244475, 14420424, 13815823, 14586841, 14868769, 15095467,
  11327182, 13105317, 14258918, 13906217
]

año=[1980+i for i in range(len(importaciones))]
# Crear el DataFrame con los componentes del PIB
df = pd.DataFrame({
    'año': año,  # Suponiendo que los datos corresponden a 44 años
    'c': [ch + cp for ch, cp in zip(consumo_hogares, consumo_publico)],  # Consumo total (hogares + gobierno)
    'fbcf': formacion_bruta_capital_fijo,  # Formación bruta de capital fijo (Inversión)
    'x': exportaciones,  # Exportaciones
    'm': importaciones,  # Importaciones
    'pib':pib
})

# Establecer el índice como el año
df.set_index('año', inplace=True)

df.head()

# %%
df_participacion=df_participacion=pd.DataFrame({
    'c':df['c']/df['pib'],
    'i':df['fbcf']/df['pib'],
    'x':df['x']/df['pib'],
    'm':df['m']/df['pib']
})
df_participacion

# %%
df_periodo1 = df_participacion.loc[1952:1974]
df_periodo2 = df_participacion.loc[1975:2005]
df_periodo3 = df_participacion.loc[2006:2025]

# Calcular estadísticas descriptivas (en este ejemplo usamos las medias)
media_p1 = {
    'c': df_periodo1['c'].mean(),
    'i': df_periodo1['i'].mean(),
    'x': df_periodo1['x'].mean(),
    'm': df_periodo1['m'].mean()
}
media_p2 = {
    'c': df_periodo2['c'].mean(),
    'i': df_periodo2['i'].mean(),
    'x': df_periodo2['x'].mean(),
    'm': df_periodo2['m'].mean()
}
media_p3 = {
    'c': df_periodo3['c'].mean(),
    'i': df_periodo3['i'].mean(),
    'x': df_periodo3['x'].mean(),
    'm': df_periodo3['m'].mean()
}
media_p2

# %%
media_p3
