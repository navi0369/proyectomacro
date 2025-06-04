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

# Definimos el mapeo de meses a un número para ordenarlos correctamente
month_order = {
    "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
    "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
    "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
}

# Lista de datos (Año, Mes, Precio)
data = [
    (1996, "Enero", 18.86),   (1996, "Febrero", 19.09), (1996, "Marzo", 21.33),
    (1996, "Abril", 23.50),  (1996, "Mayo", 21.17),    (1996, "Junio", 20.42),
    (1996, "Julio", 21.30),  (1996, "Agosto", 21.90),  (1996, "Septiembre", 23.97),
    (1996, "Octubre", 24.88),(1996, "Noviembre", 23.71),(1996, "Diciembre", 25.23),

    (1997, "Enero", 25.13),  (1997, "Febrero", 22.18), (1997, "Marzo", 20.97),
    (1997, "Abril", 19.70),  (1997, "Mayo", 20.82),    (1997, "Junio", 19.26),
    (1997, "Julio", 19.66),  (1997, "Agosto", 19.95),  (1997, "Septiembre", 19.80),
    (1997, "Octubre", 21.33),(1997, "Noviembre", 20.19),(1997, "Diciembre", 18.33),

    (1998, "Enero", 16.72),  (1998, "Febrero", 16.06), (1998, "Marzo", 15.12),
    (1998, "Abril", 15.35),  (1998, "Mayo", 14.91),    (1998, "Junio", 13.72),
    (1998, "Julio", 14.17),  (1998, "Agosto", 13.47),  (1998, "Septiembre", 15.03),
    (1998, "Octubre", 14.46),(1998, "Noviembre", 13.00),(1998, "Diciembre", 11.35),

    (1999, "Enero", 12.52),  (1999, "Febrero", 12.01), (1999, "Marzo", 14.68),
    (1999, "Abril", 17.31),  (1999, "Mayo", 17.72),    (1999, "Junio", 17.92),
    (1999, "Julio", 20.10),  (1999, "Agosto", 21.28),  (1999, "Septiembre", 23.80),
    (1999, "Octubre", 22.69),(1999, "Noviembre", 25.00),(1999, "Diciembre", 26.10),

    (2000, "Enero", 27.26),  (2000, "Febrero", 29.37), (2000, "Marzo", 29.84),
    (2000, "Abril", 25.72),  (2000, "Mayo", 28.79),    (2000, "Junio", 31.82),
    (2000, "Julio", 29.70),  (2000, "Agosto", 31.26),  (2000, "Septiembre", 33.88),
    (2000, "Octubre", 33.11),(2000, "Noviembre", 34.42),(2000, "Diciembre", 28.44),
]

# Creamos el DataFrame
df = pd.DataFrame(data, columns=["AÑO", "MES", "PRECIO"])

# Agregamos una columna auxiliar para ordenar los meses
df["ORDEN_MES"] = df["MES"].map(month_order)

# Ordenamos por año y por mes
df.sort_values(by=["AÑO", "ORDEN_MES"], inplace=True)

# Calculamos la media anual
media_anual = df.groupby("AÑO")["PRECIO"].mean().reset_index()

df.groupby("AÑO")["PRECIO"].mean()



# %%
# 1) Mapeo de meses a número para ordenar correctamente
month_order = {
    "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
    "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
    "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12
}

# 2) Datos: (AÑO, MES, PRECIO)
data = [
    (2001, "Enero", 29.59),   (2001, "Febrero", 29.61),  (2001, "Marzo", 27.25),
    (2001, "Abril", 27.49),   (2001, "Mayo", 28.63),     (2001, "Junio", 27.60),
    (2001, "Julio", 26.43),   (2001, "Agosto", 27.37),   (2001, "Septiembre", 26.20),
    (2001, "Octubre", 22.17), (2001, "Noviembre", 19.64),(2001, "Diciembre", 19.39),
    
    (2002, "Enero", 19.72),   (2002, "Febrero", 20.72),  (2002, "Marzo", 24.53),
    (2002, "Abril", 26.18),   (2002, "Mayo", 27.04),     (2002, "Junio", 25.52),
    (2002, "Julio", 26.97),   (2002, "Agosto", 28.39),   (2002, "Septiembre", 29.66),
    (2002, "Octubre", 28.84), (2002, "Noviembre", 26.35),(2002, "Diciembre", 29.46),
    
    (2003, "Enero", 32.95),   (2003, "Febrero", 35.83),  (2003, "Marzo", 33.51),
    (2003, "Abril", 28.17),   (2003, "Mayo", 28.11),     (2003, "Junio", 30.66),
    (2003, "Julio", 30.76),   (2003, "Agosto", 31.57),   (2003, "Septiembre", 28.31),
    (2003, "Octubre", 30.34), (2003, "Noviembre", 31.11),(2003, "Diciembre", 32.13),
    
    (2004, "Enero", 34.31),   (2004, "Febrero", 34.69),  (2004, "Marzo", 36.74),
    (2004, "Abril", 36.75),   (2004, "Mayo", 40.28),     (2004, "Junio", 38.03),
    (2004, "Julio", 40.78),   (2004, "Agosto", 44.90),   (2004, "Septiembre", 45.94),
    (2004, "Octubre", 53.28), (2004, "Noviembre", 48.47),(2004, "Diciembre", 43.15),
    
    (2005, "Enero", 46.84),   (2005, "Febrero", 48.15),  (2005, "Marzo", 54.19),
    (2005, "Abril", 52.98),   (2005, "Mayo", 49.83),     (2005, "Junio", 56.35),
    (2005, "Julio", 59.00),   (2005, "Agosto", 64.99),   (2005, "Septiembre", 65.59),
    (2005, "Octubre", 62.26), (2005, "Noviembre", 58.32),(2005, "Diciembre", 59.41),
]

# 3) Creación del DataFrame
df = pd.DataFrame(data, columns=["AÑO", "MES", "PRECIO"])

# 4) Añadimos columna auxiliar para ordenar los meses
df["ORDEN_MES"] = df["MES"].map(month_order)

# 5) Ordenamos por año y mes
df.sort_values(by=["AÑO", "ORDEN_MES"], inplace=True)

# 6) Calculamos la media anual y la agregamos al propio DataFrame
df["media_anual"] = df.groupby("AÑO")["PRECIO"].transform("mean")

# 7) Vemos los resultados
df.groupby("AÑO")["PRECIO"].mean()


# %%
# 2) Datos (AÑO, MES, PRECIO) - 2006 a 2010
data = [
    # 2006
    (2006, "Enero", 65.49),   (2006, "Febrero", 61.63),  (2006, "Marzo", 62.69),
    (2006, "Abril", 69.44),   (2006, "Mayo", 70.84),     (2006, "Junio", 70.95),
    (2006, "Julio", 74.41),   (2006, "Agosto", 73.04),   (2006, "Septiembre", 63.80),
    (2006, "Octubre", 58.89), (2006, "Noviembre", 59.08),(2006, "Diciembre", 61.96),

    # 2007
    (2007, "Enero", 54.51),   (2007, "Febrero", 59.28),  (2007, "Marzo", 60.44),
    (2007, "Abril", 63.98),   (2007, "Mayo", 63.46),     (2007, "Junio", 67.49),
    (2007, "Julio", 74.12),   (2007, "Agosto", 72.36),   (2007, "Septiembre", 79.92),
    (2007, "Octubre", 85.80), (2007, "Noviembre", 94.77),(2007, "Diciembre", 91.69),

    # 2008
    (2008, "Enero", 92.97),   (2008, "Febrero", 95.39),  (2008, "Marzo", 105.45),
    (2008, "Abril", 112.58),  (2008, "Mayo", 125.40),    (2008, "Junio", 133.88),
    (2008, "Julio", 133.37),  (2008, "Agosto", 116.67),  (2008, "Septiembre", 104.11),
    (2008, "Octubre", 76.61), (2008, "Noviembre", 57.31),(2008, "Diciembre", 41.12),

    # 2009
    (2009, "Enero", 41.71),   (2009, "Febrero", 39.09),  (2009, "Marzo", 47.94),
    (2009, "Abril", 49.65),   (2009, "Mayo", 59.03),     (2009, "Junio", 69.64),
    (2009, "Julio", 64.15),   (2009, "Agosto", 71.05),   (2009, "Septiembre", 69.41),
    (2009, "Octubre", 75.72), (2009, "Noviembre", 77.99),(2009, "Diciembre", 74.47),

    # 2010
    (2010, "Enero", 78.33),   (2010, "Febrero", 76.39),  (2010, "Marzo", 81.20),
    (2010, "Abril", 84.29),   (2010, "Mayo", 73.74),     (2010, "Junio", 75.34),
    (2010, "Julio", 76.32),   (2010, "Agosto", 76.60),   (2010, "Septiembre", 75.24),
    (2010, "Octubre", 81.89), (2010, "Noviembre", 84.25),(2010, "Diciembre", 89.15),
]

# 3) Creamos el DataFrame
df = pd.DataFrame(data, columns=["AÑO", "MES", "PRECIO"])

# 4) Ordenamos según el mes usando la columna auxiliar
df["ORDEN_MES"] = df["MES"].map(month_order)
df.sort_values(by=["AÑO", "ORDEN_MES"], inplace=True)

# 5) Calculamos la media anual y la agregamos al DataFrame
df["media_anual"] = df.groupby("AÑO")["PRECIO"].transform("mean")

# 6) Visualizamos
df.groupby("AÑO")["PRECIO"].mean()


# %%
# 2) Datos (AÑO, MES, PRECIO) para 2011-2015
data = [
    # 2011
    (2011, "Enero", 89.17),   (2011, "Febrero", 88.58),  (2011, "Marzo", 102.86),
    (2011, "Abril", 109.53),  (2011, "Mayo", 100.90),    (2011, "Junio", 96.26),
    (2011, "Julio", 97.30),   (2011, "Agosto", 86.33),   (2011, "Septiembre", 85.52),
    (2011, "Octubre", 86.32), (2011, "Noviembre", 97.16),(2011, "Diciembre", 98.56),

    # 2012
    (2012, "Enero", 100.27),  (2012, "Febrero", 102.20), (2012, "Marzo", 106.16),
    (2012, "Abril", 103.32),  (2012, "Mayo", 94.66),     (2012, "Junio", 82.30),
    (2012, "Julio", 87.90),   (2012, "Agosto", 94.13),   (2012, "Septiembre", 94.51),
    (2012, "Octubre", 89.49), (2012, "Noviembre", 86.53),(2012, "Diciembre", 87.86),

    # 2013
    (2013, "Enero", 94.76),   (2013, "Febrero", 95.31),  (2013, "Marzo", 92.94),
    (2013, "Abril", 92.02),   (2013, "Mayo", 94.51),     (2013, "Junio", 95.77),
    (2013, "Julio", 104.67),  (2013, "Agosto", 106.57),  (2013, "Septiembre", 106.29),
    (2013, "Octubre", 100.54),(2013, "Noviembre", 93.86),(2013, "Diciembre", 97.63),

    # 2014
    (2014, "Enero", 94.62),   (2014, "Febrero", 100.82), (2014, "Marzo", 100.80),
    (2014, "Abril", 102.07),  (2014, "Mayo", 102.18),    (2014, "Junio", 105.79),
    (2014, "Julio", 103.59),  (2014, "Agosto", 96.54),   (2014, "Septiembre", 93.21),
    (2014, "Octubre", 84.40), (2014, "Noviembre", 75.79),(2014, "Diciembre", 59.29),

    # 2015
    (2015, "Enero", 47.22),   (2015, "Febrero", 50.58),  (2015, "Marzo", 47.82),
    (2015, "Abril", 54.45),   (2015, "Mayo", 59.27),     (2015, "Junio", 59.82),
    (2015, "Julio", 50.90),   (2015, "Agosto", 42.87),   (2015, "Septiembre", 45.48),
    (2015, "Octubre", 46.22), (2015, "Noviembre", 42.44),(2015, "Diciembre", 37.19),
]

# 3) Creación del DataFrame
df = pd.DataFrame(data, columns=["AÑO", "MES", "PRECIO"])

# 4) Añadimos columna auxiliar para ordenar los meses
df["ORDEN_MES"] = df["MES"].map(month_order)

# 5) Ordenamos por AÑO y ORDEN_MES
df.sort_values(by=["AÑO", "ORDEN_MES"], inplace=True)

# 6) Calculamos la media anual y la agregamos al DataFrame
df["media_anual"] = df.groupby("AÑO")["PRECIO"].transform("mean")

# 7) Visualizamos
df.groupby("AÑO")["PRECIO"].mean()


# %%
# Datos (AÑO, MES, PRECIO) 2016 - 2020
data = [
    # 2016
    (2016, "Enero", 31.68),  (2016, "Febrero", 30.32), (2016, "Marzo", 37.55),
    (2016, "Abril", 40.75),  (2016, "Mayo", 46.71),    (2016, "Junio", 48.76),
    (2016, "Julio", 44.65),  (2016, "Agosto", 44.72),  (2016, "Septiembre", 45.18),
    (2016, "Octubre", 49.78),(2016, "Noviembre", 45.66),(2016, "Diciembre", 51.97),

    # 2017
    (2017, "Enero", 52.50),  (2017, "Febrero", 53.47), (2017, "Marzo", 49.33),
    (2017, "Abril", 51.06),  (2017, "Mayo", 48.48),    (2017, "Junio", 45.18),
    (2017, "Julio", 46.63),  (2017, "Agosto", 48.04),  (2017, "Septiembre", 49.82),
    (2017, "Octubre", 51.58),(2017, "Noviembre", 56.64),(2017, "Diciembre", 57.88),

    # 2018
    (2018, "Enero", 63.70),  (2018, "Febrero", 62.23), (2018, "Marzo", 62.73),
    (2018, "Abril", 66.25),  (2018, "Mayo", 69.98),    (2018, "Junio", 67.87),
    (2018, "Julio", 70.98),  (2018, "Agosto", 68.06),  (2018, "Septiembre", 70.23),
    (2018, "Octubre", 70.75),(2018, "Noviembre", 56.96),(2018, "Diciembre", 49.52),

    # 2019
    (2019, "Enero", 51.38),  (2019, "Febrero", 54.95), (2019, "Marzo", 58.15),
    (2019, "Abril", 63.86),  (2019, "Mayo", 60.83),    (2019, "Junio", 54.66),
    (2019, "Julio", 57.35),  (2019, "Agosto", 54.81),  (2019, "Septiembre", 56.95),
    (2019, "Octubre", 53.96),(2019, "Noviembre", 57.03),(2019, "Diciembre", 59.88),

    # 2020
    (2020, "Enero", 57.52),  (2020, "Febrero", 50.54), (2020, "Marzo", 29.21),
    (2020, "Abril", 16.55),  (2020, "Mayo", 28.56),    (2020, "Junio", 38.31),
    (2020, "Julio", 40.71),  (2020, "Agosto", 42.34),  (2020, "Septiembre", 39.63),
    (2020, "Octubre", 39.40),(2020, "Noviembre", 40.94),(2020, "Diciembre", 47.02),
]

# Creación del DataFrame
df = pd.DataFrame(data, columns=["AÑO", "MES", "PRECIO"])

# Ordenamos por mes con una columna auxiliar
df["ORDEN_MES"] = df["MES"].map(month_order)
df.sort_values(by=["AÑO", "ORDEN_MES"], inplace=True)

# Calculamos la media anual y la agregamos al DataFrame
df["media_anual"] = df.groupby("AÑO")["PRECIO"].transform("mean")

# Mostramos los datos resultantes
df.groupby("AÑO")["PRECIO"].mean()


# %%
# Datos (AÑO, MES, PRECIO) 2021 - 2023
data = [
    # 2021
    (2021, "Enero", 52.10),   (2021, "Febrero", 59.06),  (2021, "Marzo", 62.35),
    (2021, "Abril", 61.71),   (2021, "Mayo", 65.18),     (2021, "Junio", 71.38),
    (2021, "Julio", 72.46),   (2021, "Agosto", 67.73),   (2021, "Septiembre", 71.56),
    (2021, "Octubre", 81.33), (2021, "Noviembre", 79.17),(2021, "Diciembre", 71.53),

    # 2022
    (2022, "Enero", 83.13),   (2022, "Febrero", 91.76),  (2022, "Marzo", 108.58),
    (2022, "Abril", 101.78),  (2022, "Mayo", 109.60),    (2022, "Junio", 114.59),
    (2022, "Julio", 99.85),   (2022, "Agosto", 91.57),   (2022, "Septiembre", 83.87),
    (2022, "Octubre", 87.26), (2022, "Noviembre", 84.78),(2022, "Diciembre", 76.50),

    # 2023
    (2023, "Enero", 78.11),   (2023, "Febrero", 76.85),  (2023, "Marzo", 73.37),
    (2023, "Abril", 79.44),   (2023, "Mayo", 71.62),     (2023, "Junio", 70.27),
    (2023, "Julio", 76.44),   (2023, "Agosto", 81.47),   (2023, "Septiembre", 89.58),
    (2023, "Octubre", 85.57), (2023, "Noviembre", 77.44),(2023, "Diciembre", 72.09),
]

# Creamos el DataFrame
df = pd.DataFrame(data, columns=["AÑO", "MES", "PRECIO"])

# Ordenamos por mes con una columna auxiliar
df["ORDEN_MES"] = df["MES"].map(month_order)
df.sort_values(by=["AÑO", "ORDEN_MES"], inplace=True)

# Calculamos la media anual y la agregamos al DataFrame
df["media_anual"] = df.groupby("AÑO")["PRECIO"].transform("mean")

# Mostramos el resultado
df.groupby("AÑO")["PRECIO"].mean()
