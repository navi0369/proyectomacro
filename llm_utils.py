import re
from openai import OpenAI
from config import MODEL_NAME, OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

# ----------------------------- 
# Funciones de Interacción con el LLM
# -----------------------------

def generate_sql_from_question(question):
    prompt = f'''
Eres un generador de consultas SQL experto. Tu única tarea es convertir preguntas en SQL sin agregar explicaciones.
La base de datos macroeconómica contiene las siguientes tablas:

- PIB_Real_Gasto 
  - Columnas: año, gastos_consumo, formacion_capital, exportacion_bienes_servicios, importacion_bienes, pib_real_base_1990
  - Valores en: En millones de bolivianos de 1990

- Tasa_Crecimiento_PIB
  - Columnas: año, crecimiento
  - Valores en: Porcentaje

- precio_oficial_minerales
  - Columnas: año, Zinc, Estaño, Oro, Plata, Antimonio, Plomo, Wólfram, Cobre, Bismuto, Cadmio, Manganeso
  - Valores en: Dólares Americanos de 1990

- produccion_minerales
  - Columnas: año, Zinc, Estaño, Oro, Plata, Antimonio, Plomo, Wólfram, Cobre
  - Valores en: Toneladas Finas

- precio_minerales 
  - Columnas: año, Zinc, Estaño, Oro, Plata, Antimonio, Plomo, Wólfram, Cobre
  - Valores en: Dólares Americanos de 1990

- Balanza_Comercial 
  - Columnas: año, exportaciones, importaciones, saldo_comercial
  - Valores en: Millones de dólares

- Participacion_PIB 
  - Columnas: año, exportaciones_pib, importaciones_pib
  - Valores en: Porcentaje

- Reservas_oro_divisas 
  - Columnas: año, reservas_totales
  - Valores en: Millones de dólares

- grado_de_apertura
  - Columnas: año, grado
  - Valores en: Porcentaje
  - Importante: fórmula (X+M) / PIB (%)

- participacion_x_m_pib 
  - Columnas: año, X, M
  - Valores en: Porcentaje
  - Importante: X: X/PIB y M: M/PIB

- exp_trad_no_trad
  - Columnas: 
    - año
    - exp_trad: Exportaciones Tradicionales (% del total)
    - exp_no_trad: Exportaciones No Tradicionales (% del total)
  - Valores en: Porcentaje

- exportaciones_totales 
  - Columnas:  
    - año (INTEGER PRIMARY KEY)  
    - productos_tradicionales (REAL)  
    - productos_no_tradicionales (REAL)  
    - total_valor_oficial (REAL)  
  - Valores en: Millones de dólares  

- participacion_hidrocarburos_minerales_exportaciones_tradicionales
  - Columnas:  
    - año (INTEGER PRIMARY KEY)  
    - minerales (REAL)  
    - hidrocarburos (REAL)  
  - Valores en: Porcentaje  


- participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos
  - Columnas:  
    - año (INTEGER PRIMARY KEY)  
    - exportacion_gas (REAL)  
    - otros_hidrocarburos (REAL)  
  - Valores en: Porcentaje  


- composicion_importaciones_uso_destino 
  - Columnas:  
    - año (INTEGER PRIMARY KEY)  
    - bienes_consumo (REAL)  
    - materias_primas_productos_intermedios (REAL)  
    - bienes_capital (REAL)  
    - diversos (REAL)  
    - total_valor_oficial_cif (REAL)  
  - Valores en: Millones de dólares CIF  

  - Desde 2016, datos preliminares  

- participacion_composicion_importaciones_uso_destino 
  - Columnas:  
    - año (INTEGER PRIMARY KEY)  
    - bienes_consumo (REAL)  
    - materias_primas_productos_intermedios (REAL)  
    - bienes_capital (REAL)  
    - diversos (REAL)  
    - total_cif (REAL)  
  - Valores en: Porcentaje  

  - Desde 2016, datos preliminares  


Convierte la siguiente pregunta en una consulta SQL válida para SQLite:
"{question}"

Tu respuesta debe contener solo código SQL encerrado en triple comillas dobles, sin explicaciones adicionales.
'''
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Eres un generador de consultas SQL experto."},
            {"role": "user", "content": prompt}
        ]
    )
    # Acceso a la respuesta usando la nueva interfaz
    full_response = response.choices[0].message.content.strip()
    
    sql_match = re.search(r'"""(.*?)"""', full_response, re.DOTALL)
    if not sql_match:
        sql_match = re.search(r"```sql\s*(.*?)\s*```", full_response, re.DOTALL)
    if sql_match:
        sql_query = sql_match.group(1).strip()
    else:
        sql_query = full_response.strip()
    
    sql_query = sql_query.replace("`", "").replace(";", "").strip()
    return sql_query


def generate_explanation(question, sql_query, result):
    prompt = f"""
        Eres un analista de datos experto.
        Se ejecutó la siguiente consulta SQL:
        {sql_query}
        sobre una base de datos macroeconómica.
        El resultado obtenido fue: {result}.
        Ahora responde de forma clara y concisa a la pregunta:
        "{question}"
        Explica brevemente qué significa este resultado.
        Respuesta:
        """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Eres un analista de datos experto."},
            {"role": "user", "content": prompt}
        ]
    )
    explanation = response.choices[0].message.content.strip()
    return explanation