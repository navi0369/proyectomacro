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
#     display_name: .venv
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import sqlite3
import os

# 1. Directorio de salida
output_dir = "../"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "precio_oficial_minerales.xlsx")

# 2. Conexión a la base de datos y extracción
conn = sqlite3.connect('../../db/proyectomacro.db')
df = pd.read_sql_query("SELECT * FROM precio_oficial_minerales ORDER BY año", conn)
conn.close()

# 3. Exportar a Excel
df.to_excel(output_file, index=False, sheet_name="Precios Minerales")

print(f"Datos exportados a: {output_file}")


# %%
import pandas as pd
import sqlite3
import os

# 1. Directorio de salida
output_dir = "../"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "exportaciones_minerales_totales.xlsx")

# 2. Conexión a la base de datos y extracción
conn = sqlite3.connect('../../db/proyectomacro.db')
df = pd.read_sql_query("SELECT * FROM exportaciones_minerales_totales ORDER BY año", conn)
conn.close()

# 3. Exportar a Excel
df.to_excel(output_file, index=False, sheet_name="Exportaciones Minerales")

print(f"Datos exportados a: {output_file}")


# %%
import pandas as pd
import sqlite3
import os

# 1. Directorio de salida
output_dir = "../"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "exportaciones_minerales_totales.xlsx")

# 2. Conexión a la base de datos y extracción
conn = sqlite3.connect('../../db/proyectomacro.db')
df = pd.read_sql_query("SELECT * FROM exportaciones_minerales_totales ORDER BY año", conn)
conn.close()

# 3. Exportar a Excel
df.to_excel(output_file, index=False, sheet_name="Exportaciones Minerales")

print(f"Datos exportados a: {output_file}")


# %%
import pandas as pd
import sqlite3
import os

# 1. Directorio de salida
output_dir = "../"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "balanza_comercial.xlsx")

# 2. Conexión a la base de datos y extracción
conn = sqlite3.connect('../../db/proyectomacro.db')
df = pd.read_sql_query("SELECT * FROM balanza_comercial ORDER BY año", conn)
conn.close()

# 3. Exportar a Excel
df.to_excel(output_file, index=False, sheet_name="Balanza Comercial")

print(f"Datos exportados a: {output_file}")


# %%
import pandas as pd
import sqlite3
import os

# 1. Directorio de salida
output_dir = "../"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "pib_ramas.xlsx")

# 2. Conexión a la base de datos y extracción
conn = sqlite3.connect('../../db/proyectomacro.db')
df = pd.read_sql_query("SELECT * FROM pib_ramas ORDER BY año", conn)
conn.close()

# 3. Exportar a Excel
df.to_excel(output_file, index=False, sheet_name="PIB por Ramas")

print(f"Datos exportados a: {output_file}")

# %%
import pandas as pd
import sqlite3
import os

# 1. Directorio de salida
output_dir = "../"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "pib_real_gasto.xlsx")

# 2. Conexión a la base de datos y extracción
conn = sqlite3.connect('../../db/proyectomacro.db')
df = pd.read_sql_query("SELECT * FROM pib_real_gasto ORDER BY año", conn)
conn.close()

# 3. Exportar a Excel
df.to_excel(output_file, index=False, sheet_name="PIB Real por Gasto")

print(f"Datos exportados a: {output_file}")

# %%
import pandas as pd
import sqlite3
import os

# 1. Directorio de salida
output_dir = "../"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "precio_oficial_minerales.xlsx")

# 2. Conexión a la base de datos y extracción
conn = sqlite3.connect('../../db/proyectomacro.db')
df = pd.read_sql_query("SELECT * FROM precio_oficial_minerales ORDER BY año", conn)
conn.close()

# 3. Exportar a Excel
df.to_excel(output_file, index=False, sheet_name="Precios Minerales")

print(f"Datos exportados a: {output_file}")

# %%
import pandas as pd
import sqlite3
import os

# 1. Directorio de salida
output_dir = "../"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "exportaciones_minerales_totales.xlsx")

# 2. Conexión a la base de datos y extracción
conn = sqlite3.connect('../../db/proyectomacro.db')
df = pd.read_sql_query("SELECT * FROM exportaciones_minerales_totales ORDER BY año", conn)
conn.close()

# 3. Exportar a Excel
df.to_excel(output_file, index=False, sheet_name="Exportaciones Minerales Totales")

print(f"Datos exportados a: {output_file}")
