# 📊 Documentación Completa: plotter_matplotlib.py

## 🎯 Objetivo
Este documento explica **línea por línea** el funcionamiento del archivo `plotter_matplotlib.py`, que es una aplicación web interactiva construida con **Dash** para generar gráficas económicas desde una base de datos SQLite.

---

## 📋 Índice
1. [Estructura General](#estructura-general)
2. [Importaciones y Configuración](#importaciones-y-configuración)
3. [Funciones Auxiliares](#funciones-auxiliares)
4. [Layout de la Interfaz](#layout-de-la-interfaz)
5. [Callbacks Interactivos](#callbacks-interactivos)
6. [Flujo de Ejecución](#flujo-de-ejecución)
7. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## 🏗️ Estructura General

El archivo está organizado en **6 secciones principales**:

```
plotter_matplotlib.py
├── 1. Importaciones y configuración inicial
├── 2. Registro de página Dash
├── 3. Funciones auxiliares (6 funciones)
├── 4. Layout de la interfaz web
├── 5. Callbacks interactivos (3 callbacks)
└── 6. Lógica principal de generación de gráficas
```

---

## 📦 Importaciones y Configuración

### Sección 1: Docstring e Importaciones

```python
"""
Página para generar gráficas personalizadas con matplotlib
Solo líneas simples, sin anotaciones ni elementos adicionales
"""
```
**Explicación**: Docstring que describe el propósito del módulo.

```python
import dash
from dash import html, dcc, Input, Output, State, callback
```
**Explicación**: 
- `dash`: Framework principal para crear aplicaciones web interactivas
- `html`: Componentes HTML (div, h1, p, etc.)
- `dcc`: Dash Core Components (dropdown, input, slider, etc.)
- `Input, Output, State`: Decoradores para crear callbacks reactivos
- `callback`: Decorador para funciones que responden a interacciones

```python
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo para servidor
```
**Explicación**:
- `pandas`: Manipulación de datos tabulares
- `matplotlib.pyplot`: Generación de gráficas
- `matplotlib.use('Agg')`: **CRÍTICO** - Usa backend sin ventanas para servidor web

```python
import io
import base64
import sqlite3
import yaml
import os
import re
```
**Explicación**:
- `io`: Manejo de streams de datos en memoria
- `base64`: Codificación de imágenes para mostrar en web
- `sqlite3`: Conexión a base de datos SQLite
- `yaml`: Lectura de archivos de configuración
- `os`: Operaciones del sistema operativo
- `re`: Expresiones regulares para procesar texto

```python
from proyectomacro.extract_data import load_validated_tables
from func_auxiliares.config import DB_PATH
from func_auxiliares.graficos_utils import set_style, get_df, init_base_plot
```
**Explicación**: Importaciones del proyecto:
- `load_validated_tables`: Función para cargar datos validados
- `DB_PATH`: Ruta a la base de datos SQLite
- `set_style`: Aplicar estilo corporativo a gráficas
- `get_df`: Ejecutar queries SQL y obtener DataFrames
- `init_base_plot`: Función base para crear gráficas consistentes

### Sección 2: Registro de Página

```python
dash.register_page(
    __name__,
    path="/plotter-matplotlib",
    name="Generador de Gráficas",
    title="Generador de Gráficas de Serie Completa",
    description="Genera gráficas de líneas simples usando matplotlib",
)
```
**Explicación**: Registra esta página en el sistema de enrutamiento de Dash:
- `path`: URL donde estará disponible la página
- `name`: Nombre que aparece en navegación
- `title`: Título de la pestaña del navegador
- `description`: Descripción para SEO/metadatos

---

## 🔧 Funciones Auxiliares

### Función 1: `get_available_tables()`

```python
def get_available_tables():
    """Obtiene lista de tablas disponibles en la base de datos"""
    try:
        with sqlite3.connect(str(DB_PATH)) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            return sorted(tables)
    except Exception as e:
        print(f"Error obteniendo tablas: {e}")
        return []
```

**Explicación línea por línea**:
1. **Línea 3**: `with sqlite3.connect(str(DB_PATH)) as conn:` - Abre conexión a SQLite con manejo automático de cierre
2. **Línea 4**: `cursor = conn.cursor()` - Crea cursor para ejecutar comandos SQL
3. **Línea 5**: `cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")` - Query que obtiene nombres de todas las tablas
4. **Línea 6**: `tables = [row[0] for row in cursor.fetchall()]` - Extrae nombres en lista Python
5. **Línea 7**: `return sorted(tables)` - Retorna lista ordenada alfabéticamente

**Ejemplo de salida**:
```python
['PIB_Real_Gasto', 'balanza_comercial', 'exportaciones_minerales_totales', ...]
```

### Función 2: `load_table_metadata()`

```python
def load_table_metadata():
    """Carga metadata de tables_metadata.yml y pages.yml"""
    try:
        # Cargar tables_metadata.yml
        metadata_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'tables_metadata.yml')
        with open(metadata_path, 'r', encoding='utf-8') as f:
            tables_metadata = yaml.safe_load(f)
        
        # Cargar pages.yml
        pages_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'pages.yml')
        with open(pages_path, 'r', encoding='utf-8') as f:
            pages_data = yaml.safe_load(f)
        
        return tables_metadata, pages_data
    except Exception as e:
        print(f"Error cargando metadata: {e}")
        return {}, {}
```

**Explicación línea por línea**:
1. **Líneas 4-5**: Construye ruta al archivo `tables_metadata.yml` usando ruta relativa
2. **Líneas 6-7**: Abre y carga el archivo YAML con metadata de columnas
3. **Líneas 9-12**: Hace lo mismo para `pages.yml` que contiene info de secciones
4. **Línea 14**: Retorna ambos diccionarios cargados
5. **Líneas 15-17**: Manejo de errores, retorna diccionarios vacíos si falla

**Ejemplo de datos cargados**:
```python
# tables_metadata ejemplo:
{
    'tables': {
        'PIB_Real_Gasto': {
            'consumo_privado': {'unit': 'Miles de Bs 1990', 'type': 'monetary'},
            'pib_real': {'unit': 'Miles de Bs 1990', 'type': 'monetary'}
        }
    }
}

# pages_data ejemplo:
{
    'secciones': {
        'cuentas_nacionales': {
            'name': 'Cuentas Nacionales',
            'tablas': {
                'pib_real_gasto': {
                    'tabla': 'PIB_Real_Gasto',
                    'label': 'PIB real por componentes de gasto',
                    'metadata': {'periodo': '1950 – 2023'}
                }
            }
        }
    }
}
```

### Función 3: `get_table_details(table_name)`

```python
def get_table_details(table_name):
    """Extrae detalles importantes de una tabla específica"""
    tables_metadata, pages_data = load_table_metadata()
    
    details = {
        'table_name': table_name,
        'description': 'No disponible',
        'period': 'No disponible',
        'unit': 'No disponible',
        'columns_info': {},
        'section': 'No disponible'
    }
```

**Explicación**:
1. **Línea 3**: Carga metadata de ambos archivos YAML
2. **Líneas 5-12**: Inicializa diccionario con valores por defecto para evitar errores

```python
    # Buscar en pages.yml
    for section_name, section_data in pages_data.get('secciones', {}).items():
        if 'tablas' in section_data:
            for tabla_key, tabla_info in section_data['tablas'].items():
                if tabla_info.get('tabla') == table_name or tabla_key == table_name.lower():
                    details['description'] = tabla_info.get('label', 'No disponible')
                    details['section'] = section_data.get('name', section_name)
                    
                    metadata = tabla_info.get('metadata', {})
                    details['period'] = metadata.get('periodo', 'No disponible')
                    details['unit'] = metadata.get('unidad', 'No disponible')
                    break
```

**Explicación del bucle de búsqueda**:
1. **Línea 14**: Itera sobre cada sección en pages.yml
2. **Línea 15**: Verifica que la sección tenga tablas
3. **Línea 16**: Itera sobre cada tabla en la sección
4. **Línea 17**: Busca coincidencia con el nombre de tabla solicitado
5. **Líneas 18-23**: Extrae información si encuentra coincidencia
6. **Línea 24**: Sale del bucle al encontrar la primera coincidencia

```python
    # Buscar en tables_metadata.yml para información de columnas
    table_metadata = tables_metadata.get('tables', {}).get(table_name, {})
    if table_metadata:
        for col_name, col_info in table_metadata.items():
            if col_name != 'año' and isinstance(col_info, dict):
                details['columns_info'][col_name] = {
                    'type': col_info.get('type', 'unknown'),
                    'unit': col_info.get('unit', 'No especificada'),
                    'scale': col_info.get('scale', 1),
                    'currency': col_info.get('currency', None),
                    'base_year': col_info.get('base_year', None)
                }
    
    return details
```

**Explicación de extracción de columnas**:
1. **Línea 26**: Accede anidadamente a la tabla específica
2. **Línea 28**: Itera sobre cada columna de la tabla
3. **Línea 29**: Excluye la columna 'año' y verifica que sea diccionario
4. **Líneas 30-36**: Extrae metadatos de cada columna con valores por defecto

**Ejemplo de salida**:
```python
{
    'table_name': 'PIB_Real_Gasto',
    'description': 'PIB real por componentes de gasto',
    'period': '1950 – 2023',
    'unit': 'Miles de bolivianos constantes de 1990',
    'section': 'Cuentas Nacionales',
    'columns_info': {
        'consumo_privado': {
            'type': 'monetary',
            'unit': 'Miles de Bs 1990',
            'scale': 1000,
            'currency': 'BOB',
            'base_year': 1990
        }
    }
}
```

### Función 4: `get_table_columns(table_name)`

```python
def get_table_columns(table_name):
    """Obtener columnas de una tabla específica"""
    try:
        query = f"PRAGMA table_info({table_name})"
        columns_df = get_df(query, conn_str=str(DB_PATH))
        return columns_df['name'].tolist()
    except Exception as e:
        print(f"Error obteniendo columnas de {table_name}: {e}")
        return []
```

**Explicación**:
1. **Línea 4**: `PRAGMA table_info()` es un comando SQLite que describe la estructura de una tabla
2. **Línea 5**: Ejecuta el query y obtiene DataFrame con info de columnas
3. **Línea 6**: Extrae solo los nombres de columnas como lista Python

**Ejemplo de PRAGMA table_info output**:
```
cid | name           | type | notnull | dflt_value | pk
----|----------------|------|---------|------------|----
0   | año            | INT  | 0       | NULL       | 0
1   | consumo_privado| REAL | 0       | NULL       | 0
2   | pib_real       | REAL | 0       | NULL       | 0
```

**Resultado de la función**:
```python
['año', 'consumo_privado', 'pib_real']
```

### Función 5: `extract_year_range(period_text)`

```python
def extract_year_range(period_text):
    """
    Extrae el rango de años de un string de período.
    Ejemplos: '1950 – 2023' -> (1950, 2023)
             '2006-2014' -> (2006, 2014)  
    """
    if not period_text or period_text == 'No disponible':
        return None, None
    
    # Buscar patrón con guión o dash
    pattern = r'(\d{4})\s*[–\-]\s*(\d{4})'
    match = re.search(pattern, period_text)
    
    if match:
        start_year = int(match.group(1))
        end_year = int(match.group(2))
        return start_year, end_year
    
    # Si no encuentra patrón, buscar años individuales
    pattern_single = r'(\d{4})'
    matches = re.findall(pattern_single, period_text)
    if matches:
        years = [int(year) for year in matches]
        return min(years), max(years)
    
    return None, None
```

**Explicación de expresiones regulares**:
1. **Línea 6**: Validación de entrada
2. **Línea 9**: `r'(\d{4})\s*[–\-]\s*(\d{4})'` - Patrón regex explicado:
   - `\d{4}`: Exactamente 4 dígitos (año)
   - `\s*`: Cero o más espacios
   - `[–\-]`: Guión largo (–) o guión corto (-)
   - Los paréntesis `()` crean grupos para capturar
3. **Líneas 12-15**: Si encuentra el patrón, extrae años de los grupos
4. **Líneas 17-22**: Plan B: busca cualquier secuencia de 4 dígitos y toma min/max

**Ejemplos de funcionamiento**:
```python
extract_year_range('1950 – 2023')     # (1950, 2023)
extract_year_range('2006-2014')       # (2006, 2014)
extract_year_range('1980   -   2020') # (1980, 2020)
extract_year_range('Período 1995 hasta 2010') # (1995, 2010)
extract_year_range('No disponible')   # (None, None)
```

### Función 6: `matplotlib_to_base64(fig)`

```python
def matplotlib_to_base64(fig):
    """Convierte figura matplotlib a string base64 para mostrar en Dash"""
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close(fig)  # Importante: cerrar figura para liberar memoria
    return f"data:image/png;base64,{image_base64}"
```

**Explicación paso a paso**:
1. **Línea 3**: `io.BytesIO()` - Crea buffer en memoria (como archivo temporal)
2. **Línea 4**: `fig.savefig()` - Guarda la figura matplotlib en el buffer como PNG
   - `dpi=300`: Alta resolución
   - `bbox_inches='tight'`: Recorta espacios en blanco
3. **Línea 5**: `buffer.seek(0)` - Mueve cursor al inicio del buffer
4. **Línea 6**: Codifica bytes de imagen a string base64
5. **Línea 7**: Cierra buffer para liberar memoria
6. **Línea 8**: **CRÍTICO** - Cierra figura matplotlib para evitar memory leaks
7. **Línea 9**: Retorna string en formato Data URL para HTML

**Ejemplo de salida**:
```
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAD...
```

### Función 7: `create_simple_lineplot(df, columns, title)`

```python
def create_simple_lineplot(df, columns, title="Gráfica de Serie Completa"):
    """
    Crea gráfica de líneas usando la misma lógica que en notebooks/serie_completa
    Sin anotaciones, medias, tasas, ni elementos adicionales
    """
    # 1. Aplicar estilo corporativo
    set_style()
    
    # 2. Preparar componentes como en los notebooks
    # Crear tuplas (columna, etiqueta) para cada columna seleccionada
    componentes = [(col, col) for col in columns if col in df.columns]
    
    # 3. Definir colores corporativos - solo para columnas que existen
    available_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    colors = {}
    for i, col in enumerate(columns):
        if col in df.columns:
            colors[col] = available_colors[i % len(available_colors)]
    
    # 4. Usar init_base_plot exactamente como en los notebooks
    fig, ax = init_base_plot(
        df=df,
        series=componentes,           # Lista de tuplas (columna, etiqueta)
        colors=colors,                # Diccionario de colores
        title=title,
        xlabel="Año",
        ylabel="Valores",
        source_text="Fuente: Base de datos del proyecto",
        figsize=(14, 8),             # Tamaño de figura
        legend_loc="upper left"       # Ubicación de leyenda
    )
    
    # 5. Ajustes finales como en los notebooks
    plt.tight_layout()
    
    return fig
```

**Explicación detallada**:

**Paso 1 - Estilo corporativo**:
```python
set_style()
```
- Aplica estilos predefinidos (colores, fuentes, etc.)

**Paso 2 - Preparar componentes**:
```python
componentes = [(col, col) for col in columns if col in df.columns]
```
- Crea lista de tuplas `(nombre_columna, etiqueta_display)`
- Solo incluye columnas que realmente existen en el DataFrame
- **Ejemplo**: `[('consumo_privado', 'consumo_privado'), ('pib_real', 'pib_real')]`

**Paso 3 - Asignar colores**:
```python
available_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
colors = {}
for i, col in enumerate(columns):
    if col in df.columns:
        colors[col] = available_colors[i % len(available_colors)]
```
- Define paleta de 5 colores corporativos
- Asigna colores cíclicamente usando operador módulo `%`
- **Ejemplo**: `{'consumo_privado': '#1f77b4', 'pib_real': '#ff7f0e'}`

**Paso 4 - Crear gráfica base**:
```python
fig, ax = init_base_plot(
    df=df,
    series=componentes,
    colors=colors,
    title=title,
    xlabel="Año",
    ylabel="Valores",
    source_text="Fuente: Base de datos del proyecto",
    figsize=(14, 8),
    legend_loc="upper left"
)
```
- Usa función corporativa `init_base_plot()` para consistencia
- Configura todos los elementos de la gráfica

**Paso 5 - Ajustes finales**:
```python
plt.tight_layout()
```
- Optimiza espaciado de elementos en la figura

---

## 🎨 Layout de la Interfaz

### Estructura del Layout

```python
layout = html.Div([
    html.Div([
        # Contenido principal
    ], style={
        'max-width': '1200px',
        'margin': '0 auto',
        'padding': '20px',
        'background-color': '#f8f9fa',
        'border-radius': '10px',
        'box-shadow': '0 2px 10px rgba(0,0,0,0.1)'
    })
])
```

**Explicación del contenedor principal**:
- `max-width: 1200px`: Limita ancho máximo
- `margin: 0 auto`: Centra horizontalmente
- `background-color: #f8f9fa`: Color gris claro
- `border-radius: 10px`: Esquinas redondeadas
- `box-shadow`: Sombra sutil para profundidad

### Componente 1: Título Principal

```python
html.H3("Generador de Gráficas de Serie Completa", 
        style={'text-align': 'center', 'color': '#2E4B8A', 'margin-bottom': '30px'})
```
- `H3`: Encabezado de nivel 3
- `#2E4B8A`: Color azul corporativo
- Centrado con margen inferior

### Componente 2: Selector de Tabla

```python
html.Div([
    html.Label("Seleccionar Tabla:", style={'font-weight': 'bold', 'margin-bottom': '10px'}),
    dcc.Dropdown(
        id='table-selector',
        options=[{'label': table, 'value': table} for table in get_available_tables()],
        placeholder="Selecciona una tabla...",
        style={'margin-bottom': '20px'}
    )
])
```

**Explicación**:
1. `html.Label`: Etiqueta descriptiva en negrita
2. `dcc.Dropdown`: Componente dropdown de Dash
3. `id='table-selector'`: Identificador único para callbacks
4. `options`: Lista generada dinámicamente llamando `get_available_tables()`
5. `placeholder`: Texto de ayuda

**Estructura de options**:
```python
[
    {'label': 'PIB_Real_Gasto', 'value': 'PIB_Real_Gasto'},
    {'label': 'balanza_comercial', 'value': 'balanza_comercial'},
    ...
]
```

### Componente 3: Panel de Detalles (Dinámico)

```python
html.Div(
    id='table-details-panel',
    style={'margin-bottom': '20px'}
)
```
- **Contenedor vacío**: Se llena dinámicamente vía callback
- **ID importante**: `table-details-panel` usado en callback

### Componente 4: Selector de Rango de Años (Dinámico)

```python
html.Div(
    id='year-range-container',
    style={'margin-bottom': '20px'}
)
```
- **Contenedor vacío**: Se llena con RangeSlider vía callback
- **Funcionalidad**: Permitirá filtrar años de los datos

### Componente 5: Selector de Columnas

```python
html.Div([
    html.Label("Seleccionar Columnas (máximo 5):", style={'font-weight': 'bold', 'margin-bottom': '10px'}),
    dcc.Dropdown(
        id='columns-selector',
        multi=True,
        placeholder="Primero selecciona una tabla...",
        style={'margin-bottom': '20px'}
    )
])
```

**Características especiales**:
- `multi=True`: Permite selección múltiple
- `id='columns-selector'`: Para callbacks
- **Sin opciones iniciales**: Se llenan dinámicamente

### Componente 6: Título Personalizado

```python
html.Div([
    html.Label("Título de la Gráfica:", style={'font-weight': 'bold', 'margin-bottom': '10px'}),
    dcc.Input(
        id='chart-title',
        type='text',
        placeholder="Título personalizado (opcional)",
        style={'width': '100%', 'padding': '8px', 'margin-bottom': '20px'}
    )
])
```

**Explicación**:
- `dcc.Input`: Campo de texto
- `type='text'`: Tipo de input
- `width: 100%`: Ocupa todo el ancho disponible
- **Opcional**: El usuario puede dejarlo vacío

### Componente 7: Botón de Generar

```python
html.Div([
    html.Button(
        "Generar Gráfica", 
        id='generate-button',
        n_clicks=0,
        style={
            'background-color': '#2E4B8A',
            'color': 'white',
            'border': 'none',
            'padding': '12px 24px',
            'font-size': '16px',
            'border-radius': '5px',
            'cursor': 'pointer',
            'margin-bottom': '20px'
        }
    )
], style={'text-align': 'center'})
```

**Explicación de propiedades**:
- `n_clicks=0`: Contador de clics (importante para callbacks)
- `id='generate-button'`: Identificador para callback
- **Estilos**: Botón azul corporativo con hover effect

### Componente 8: Mensaje de Estado

```python
html.Div(id='status-message', style={'margin-bottom': '20px'})
```
- **Contenedor vacío**: Se llena con mensajes de éxito/error
- **Feedback visual**: Informa al usuario sobre el resultado

### Componente 9: Contenedor de Gráfica

```python
html.Div(id='chart-container', style={'text-align': 'center'})
```
- **Contenedor principal**: Donde aparece la gráfica generada
- **Centrado**: Para mejor presentación visual

---

## ⚡ Callbacks Interactivos

Los callbacks son el corazón de la interactividad en Dash. Cada callback es una función que se ejecuta cuando cambian ciertos inputs.

### Callback 1: Actualizar Opciones de Columnas

```python
@callback(
    Output('columns-selector', 'options'),
    Output('columns-selector', 'value'),
    Input('table-selector', 'value'),
    prevent_initial_call=True
)
def update_columns_options(selected_table):
```

**Anatomía del decorador**:
- `Output('columns-selector', 'options')`: Actualiza las opciones del dropdown de columnas
- `Output('columns-selector', 'value')`: Limpia la selección actual
- `Input('table-selector', 'value')`: Se dispara cuando cambia la tabla seleccionada
- `prevent_initial_call=True`: No ejecuta al cargar la página

**Lógica de la función**:
```python
def update_columns_options(selected_table):
    if not selected_table:
        return [], []
    
    try:
        # Usar get_table_columns igual que en calculadora.py
        columns = get_table_columns(selected_table)
        # Filtrar columnas numéricas típicas (excluir año que suele ser índice)
        numeric_columns = [col for col in columns if col.lower() not in ['año', 'year', 'fecha', 'date']]
        
        options = [{"label": col, "value": col} for col in numeric_columns]
        return options, []
    except Exception as e:
        print(f"Error obteniendo columnas: {e}")
        return [], []
```

**Explicación paso a paso**:
1. **Línea 2**: Si no hay tabla seleccionada, limpia opciones
2. **Línea 5**: Obtiene todas las columnas de la tabla usando SQL PRAGMA
3. **Línea 7**: Filtra columnas que típicamente son fechas/años
4. **Línea 9**: Convierte a formato requerido por Dropdown
5. **Línea 10**: Retorna opciones nuevas y limpia selección actual

**Ejemplo de flujo**:
```
Usuario selecciona "PIB_Real_Gasto" 
    ↓
get_table_columns() retorna: ['año', 'consumo_privado', 'inversion_bruta_fija', 'pib_real']
    ↓
Filtrado: ['consumo_privado', 'inversion_bruta_fija', 'pib_real']
    ↓
Opciones: [
    {'label': 'consumo_privado', 'value': 'consumo_privado'},
    {'label': 'inversion_bruta_fija', 'value': 'inversion_bruta_fija'},
    {'label': 'pib_real', 'value': 'pib_real'}
]
```

### Callback 2: Generar Selector de Rango de Años

```python
@callback(
    Output('year-range-container', 'children'),
    Input('table-selector', 'value'),
    prevent_initial_call=True
)
def update_year_range_selector(selected_table):
```

**Propósito**: Crea dinámicamente un RangeSlider con el rango de años apropiado para cada tabla.

```python
def update_year_range_selector(selected_table):
    if not selected_table:
        return []
    
    try:
        # Obtener detalles de la tabla
        details = get_table_details(selected_table)
        period = details.get('period', 'No disponible')
        
        # Extraer rango de años
        start_year, end_year = extract_year_range(period)
        
        if start_year and end_year:
            return html.Div([
                html.Label(f"Rango de Años (Período disponible: {period}):", 
                          style={'font-weight': 'bold', 'margin-bottom': '10px'}),
                dcc.RangeSlider(
                    id='year-range-slider',
                    min=start_year,
                    max=end_year,
                    value=[start_year, end_year],
                    marks={year: str(year) for year in range(start_year, end_year + 1, max(1, (end_year - start_year) // 10))},
                    step=1,
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ])
        else:
            return html.Div([
                html.Label("Rango de Años:", style={'font-weight': 'bold', 'margin-bottom': '10px'}),
                html.P(f"No se pudo extraer rango de años del período: {period}", 
                      style={'color': 'orange', 'font-style': 'italic'})
            ])
            
    except Exception as e:
        return html.Div([
            html.P(f"Error generando selector de años: {str(e)}", 
                  style={'color': 'red'})
        ])
```

**Explicación detallada**:

**Líneas 5-8**: Obtención de metadata
```python
details = get_table_details(selected_table)
period = details.get('period', 'No disponible')
start_year, end_year = extract_year_range(period)
```
- Obtiene detalles de la tabla desde YAML
- Extrae el texto del período (ej: "1950 – 2023")
- Usa regex para convertir a años numéricos

**Líneas 10-22**: Creación del RangeSlider
```python
dcc.RangeSlider(
    id='year-range-slider',
    min=start_year,
    max=end_year,
    value=[start_year, end_year],
    marks={year: str(year) for year in range(start_year, end_year + 1, max(1, (end_year - start_year) // 10))},
    step=1,
    tooltip={"placement": "bottom", "always_visible": True}
)
```

**Explicación de parámetros**:
- `min/max`: Límites del slider
- `value`: Valores iniciales seleccionados
- `marks`: Marcas en el slider calculadas dinámicamente
- `step=1`: Incrementos de un año
- `tooltip`: Muestra valores al interactuar

**Cálculo de marks**:
```python
marks={year: str(year) for year in range(start_year, end_year + 1, max(1, (end_year - start_year) // 10))}
```
- `range(start_year, end_year + 1, ...)`: Desde año inicial hasta final
- `max(1, (end_year - start_year) // 10)`: Paso calculado para mostrar ~10 marcas
- **Ejemplo**: Para período 1950-2023 (73 años), paso = 7, marcas cada 7 años

**Ejemplo de flujo**:
```
Usuario selecciona "PIB_Real_Gasto"
    ↓
get_table_details() encuentra período: "1950 – 2023"
    ↓
extract_year_range() retorna: (1950, 2023)
    ↓
RangeSlider creado con:
- min: 1950
- max: 2023  
- value: [1950, 2023]
- marks: {1950: '1950', 1957: '1957', ..., 2023: '2023'}
```

### Callback 3: Mostrar Detalles de la Tabla

```python
@callback(
    Output('table-details-panel', 'children'),
    Input('table-selector', 'value'),
    prevent_initial_call=True
)
def show_table_details(selected_table):
```

**Propósito**: Muestra información completa sobre la tabla seleccionada en un panel informativo.

```python
def show_table_details(selected_table):
    if not selected_table:
        return []
    
    try:
        details = get_table_details(selected_table)
        print(details)  # Debugging
        # Crear panel de información
        info_panel = html.Div([
            html.Div([
                html.H4(f"📊 Información de la Tabla: {selected_table}", 
                       style={'color': '#2E4B8A', 'margin-bottom': '15px'}),
                
                # Información básica
                html.Div([
                    html.Div([
                        html.Strong("Descripción: "),
                        html.Span(details['description'])
                    ], style={'margin-bottom': '8px'}),
                    
                    html.Div([
                        html.Strong("Sección: "),
                        html.Span(details['section'])
                    ], style={'margin-bottom': '8px'}),
                    
                    html.Div([
                        html.Strong("Período: "),
                        html.Span(details['period'])
                    ], style={'margin-bottom': '8px'}),
                    
                    html.Div([
                        html.Strong("Unidad Principal: "),
                        html.Span(details['unit'])
                    ], style={'margin-bottom': '15px'}),
                ]),
                
                # Información de columnas disponibles (si existe)
                html.Div([
                    html.H5("📈 Columnas Disponibles:", style={'color': '#2E4B8A', 'margin-bottom': '10px'}),
                    html.Div([
                        html.Div([
                            html.Strong(f"{col_name}: "),
                            html.Span(f"{col_info['type']} - {col_info['unit']}")
                        ], style={'margin-bottom': '5px'})
                        for col_name, col_info in details['columns_info'].items()
                    ]) if details['columns_info'] else html.Span("Información de columnas no disponible", 
                                                                style={'font-style': 'italic', 'color': '#666'})
                ])
                
            ], style={
                'background-color': '#f8f9fa',
                'border': '1px solid #dee2e6',
                'border-radius': '8px',
                'padding': '15px',
                'margin-bottom': '10px'
            })
        ])
        
        return info_panel
        
    except Exception as e:
        error_panel = html.Div([
            html.Div(f"⚠️ Error cargando detalles de la tabla: {str(e)}", 
                    style={'color': 'orange', 'font-weight': 'bold'})
        ])
        return error_panel
```

**Estructura del panel generado**:

1. **Encabezado**: Título con emoji y nombre de tabla
2. **Información básica**: 4 campos principales
   - Descripción
   - Sección
   - Período  
   - Unidad principal
3. **Columnas disponibles**: Lista detallada de cada columna
4. **Manejo de errores**: Panel de error si algo falla

**Ejemplo de panel generado**:
```
📊 Información de la Tabla: PIB_Real_Gasto

Descripción: PIB real por componentes de gasto
Sección: Cuentas Nacionales
Período: 1950 – 2023
Unidad Principal: Miles de bolivianos constantes de 1990

📈 Columnas Disponibles:
consumo_privado: monetary - Miles de Bs 1990
inversion_bruta_fija: monetary - Miles de Bs 1990
pib_real: monetary - Miles de Bs 1990
```

### Callback 4: Generar Gráfica (Principal)

```python
@callback(
    Output('chart-container', 'children'),
    Output('status-message', 'children'),
    Input('generate-button', 'n_clicks'),
    State('table-selector', 'value'),
    State('columns-selector', 'value'),
    State('chart-title', 'value')
)
def generate_chart(n_clicks, selected_table, selected_columns, custom_title):
```

**Diferencia entre Input y State**:
- `Input`: Dispara el callback cuando cambia
- `State`: Solo proporciona el valor actual, no dispara

**Este callback se dispara solo cuando se hace clic en el botón**.

```python
def generate_chart(n_clicks, selected_table, selected_columns, custom_title):
    if n_clicks == 0:
        return [], ""
    
    # Validaciones
    if not selected_table:
        return [], html.Div("❌ Por favor selecciona una tabla", style={'color': 'red'})
    
    if not selected_columns:
        return [], html.Div("❌ Por favor selecciona al menos una columna", style={'color': 'red'})
    
    if len(selected_columns) > 5:
        return [], html.Div("❌ Máximo 5 columnas permitidas", style={'color': 'red'})
```

**Validaciones iniciales**:
1. **n_clicks == 0**: No hacer nada si no se ha clicado
2. **selected_table**: Verificar que hay tabla seleccionada
3. **selected_columns**: Verificar que hay columnas seleccionadas
4. **len(selected_columns) > 5**: Limitar a máximo 5 columnas

```python
    try:
        # Cargar datos usando get_df igual que en calculadora.py
        query = f"SELECT * FROM {selected_table}"
        df = get_df(query, conn_str=str(DB_PATH))
        
        # Verificar que existe columna de año
        year_col = None
        for col in ['año', 'ano', 'year']:
            if col in df.columns:
                year_col = col
                break
        
        if year_col:
            df = df.set_index(year_col)
```

**Carga y preparación de datos**:
1. **Query SQL**: Selecciona todos los datos de la tabla
2. **get_df()**: Ejecuta query y retorna DataFrame
3. **Búsqueda de columna año**: Busca diferentes variantes del nombre
4. **set_index()**: Usa la columna año como índice del DataFrame

```python
        # Verificar que las columnas seleccionadas existen
        missing_cols = [col for col in selected_columns if col not in df.columns]
        if missing_cols:
            return [], html.Div(f"❌ Columnas no encontradas: {missing_cols}", style={'color': 'red'})
        
        # Filtrar solo las columnas seleccionadas
        df_plot = df[selected_columns].copy()
        
        # Convertir a numérico y eliminar NaN
        for col in selected_columns:
            df_plot[col] = pd.to_numeric(df_plot[col], errors='coerce')
        
        df_plot = df_plot.dropna()
        
        if df_plot.empty:
            return [], html.Div("❌ No hay datos válidos para graficar", style={'color': 'red'})
```

**Procesamiento de datos**:
1. **Verificación de existencia**: Confirma que las columnas existen
2. **Filtrado**: Crea DataFrame solo con columnas seleccionadas
3. **Conversión numérica**: `pd.to_numeric(errors='coerce')` convierte a números, NaN si falla
4. **Limpieza**: Elimina filas con valores faltantes
5. **Validación final**: Verifica que quedan datos para graficar

```python
        # Generar título
        if custom_title:
            title = custom_title
        else:
            title = f"{selected_table} - {', '.join(selected_columns[:3])}"
            if len(selected_columns) > 3:
                title += "..."
```

**Generación de título**:
- Si hay título personalizado, lo usa
- Si no, genera automáticamente con nombre de tabla + primeras 3 columnas
- Añade "..." si hay más de 3 columnas

```python
        # Crear gráfica
        fig = create_simple_lineplot(df_plot, selected_columns, title)
        
        # Convertir a base64
        img_base64 = matplotlib_to_base64(fig)
        
        # Retornar imagen
        chart_img = html.Img(
            src=img_base64,
            style={'max-width': '100%', 'height': 'auto', 'border': '1px solid #ddd', 'border-radius': '5px'}
        )
        
        success_msg = html.Div(
            f"✅ Gráfica generada exitosamente: {len(df_plot)} puntos de datos",
            style={'color': 'green', 'font-weight': 'bold'}
        )
        
        return chart_img, success_msg
```

**Generación y retorno**:
1. **create_simple_lineplot()**: Crea figura matplotlib
2. **matplotlib_to_base64()**: Convierte a string base64
3. **html.Img()**: Crea elemento imagen HTML
4. **Mensaje de éxito**: Informa cantidad de puntos graficados
5. **Return**: Retorna imagen y mensaje (2 outputs)

---

## 🔄 Flujo de Ejecución Completo

### Flujo Típico del Usuario

```
1. Usuario carga la página
   ↓
2. get_available_tables() llena dropdown de tablas
   ↓
3. Usuario selecciona tabla "PIB_Real_Gasto"
   ↓
4. DISPARA 3 callbacks:
   a) update_columns_options() - llena columnas disponibles
   b) update_year_range_selector() - crea slider de años
   c) show_table_details() - muestra panel informativo
   ↓
5. Usuario selecciona columnas: ["consumo_privado", "pib_real"]
   ↓
6. Usuario ajusta rango de años: [1990, 2020]
   ↓
7. Usuario pone título: "Evolución del PIB y Consumo"
   ↓
8. Usuario hace clic en "Generar Gráfica"
   ↓
9. DISPARA generate_chart():
   a) Valida inputs
   b) Carga datos de SQLite
   c) Procesa DataFrame
   d) Filtra por años seleccionados (si implementado)
   e) Crea gráfica matplotlib
   f) Convierte a base64
   g) Muestra imagen + mensaje
```

### Ejemplo de Datos en Cada Paso

**Paso 3 - Selección de tabla**:
```python
selected_table = "PIB_Real_Gasto"
```

**Paso 4a - update_columns_options()**:
```python
# Input:
selected_table = "PIB_Real_Gasto"

# Procesamiento:
columns = ['año', 'consumo_privado', 'inversion_bruta_fija', 'exportaciones', 'importaciones', 'pib_real']
numeric_columns = ['consumo_privado', 'inversion_bruta_fija', 'exportaciones', 'importaciones', 'pib_real']

# Output:
options = [
    {'label': 'consumo_privado', 'value': 'consumo_privado'},
    {'label': 'inversion_bruta_fija', 'value': 'inversion_bruta_fija'},
    {'label': 'exportaciones', 'value': 'exportaciones'},
    {'label': 'importaciones', 'value': 'importaciones'},
    {'label': 'pib_real', 'value': 'pib_real'}
]
```

**Paso 4b - update_year_range_selector()**:
```python
# Input:
selected_table = "PIB_Real_Gasto"

# Procesamiento:
details = {
    'period': '1950 – 2023',
    'description': 'PIB real por componentes de gasto',
    ...
}
start_year, end_year = extract_year_range('1950 – 2023')  # (1950, 2023)

# Output: RangeSlider component creado dinámicamente
```

**Paso 9 - generate_chart()**:
```python
# Inputs:
n_clicks = 1
selected_table = "PIB_Real_Gasto"
selected_columns = ["consumo_privado", "pib_real"]
custom_title = "Evolución del PIB y Consumo"

# Query ejecutado:
"SELECT * FROM PIB_Real_Gasto"

# DataFrame resultante:
#      consumo_privado  pib_real
# año                          
# 1950          12500     45000
# 1951          13200     47000
# ...
# 2023          89000    185000

# DataFrame filtrado:
df_plot = df[["consumo_privado", "pib_real"]]  # Solo columnas seleccionadas

# Gráfica generada con:
# - 74 puntos de datos (1950-2023)
# - 2 líneas (consumo_privado, pib_real)
# - Título: "Evolución del PIB y Consumo"
# - Colores: consumo_privado=#1f77b4, pib_real=#ff7f0e
```

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Análisis de Exportaciones

**Objetivo**: Graficar evolución de exportaciones de minerales específicos.

**Pasos**:
1. Seleccionar tabla: `exportaciones_minerales_totales`
2. Columnas aparecen: `[estaño_valor, oro_valor, zinc_valor, plomo_valor]`
3. Seleccionar: `[oro_valor, estaño_valor]`
4. Ajustar años: `[2000, 2023]`
5. Título: "Exportaciones de Oro y Estaño (2000-2023)"

**Resultado**: Gráfica con 2 líneas mostrando evolución del valor de exportaciones.

### Ejemplo 2: Comparación PIB Sectorial

**Objetivo**: Analizar participación de sectores en el PIB.

**Pasos**:
1. Seleccionar tabla: `participacion_pib_ramas`
2. Columnas: `[agropecuario, mineria, manufactura, servicios]`
3. Seleccionar todas las columnas
4. Rango completo: `[1950, 2023]`
5. Título automático: "participacion_pib_ramas - agropecuario, mineria, manufactura..."

**Resultado**: Gráfica con 4 líneas mostrando % de participación de cada sector.

### Ejemplo 3: Análisis de Crisis Económica

**Objetivo**: Focalizar en período de crisis específico.

**Pasos**:
1. Seleccionar tabla: `tasa_crecimiento_pib`
2. Columna: `[tasa_crecimiento]`
3. **Filtro temporal clave**: `[2008, 2012]` (crisis financiera global)
4. Título: "Impacto de la Crisis 2008 en Bolivia"

**Resultado**: Gráfica de una línea mostrando variación del PIB durante la crisis.

---

## 🔧 Consideraciones Técnicas

### Gestión de Memoria

```python
plt.close(fig)  # Importante: cerrar figura para liberar memoria
```
**Crítico**: Sin esto, matplotlib acumula figuras en memoria causando memory leaks.

### Seguridad SQL

```python
query = f"SELECT * FROM {selected_table}"
```
**Potencial riesgo**: SQL injection si `selected_table` viene de usuario no confiable.
**Mitigación actual**: Las tablas vienen de dropdown pre-poblado desde la DB.

### Manejo de Errores

Cada función crítica tiene try/except:
```python
try:
    # Operación crítica
    result = risky_operation()
    return result
except Exception as e:
    print(f"Error: {e}")
    return safe_default
```

### Performance

- **Caché de metadata**: Los archivos YAML se leen cada vez (podría optimizarse)
- **Query optimization**: Se cargan todas las columnas aunque solo se usen algunas
- **Image size**: DPI=300 genera imágenes de alta calidad pero pesadas

---

## 🚀 Posibles Mejoras

### 1. Filtrado por Rango de Años

**Estado actual**: El RangeSlider se crea pero no se usa en el callback principal.

**Implementación sugerida**:
```python
# En generate_chart(), agregar:
@callback(
    Output('chart-container', 'children'),
    Output('status-message', 'children'),
    Input('generate-button', 'n_clicks'),
    State('table-selector', 'value'),
    State('columns-selector', 'value'),
    State('chart-title', 'value'),
    State('year-range-slider', 'value')  # AÑADIR ESTE STATE
)
def generate_chart(n_clicks, selected_table, selected_columns, custom_title, year_range):
    # ... código existente ...
    
    # AÑADIR después de df_plot = df_plot.dropna():
    if year_range and len(year_range) == 2:
        start_year, end_year = year_range
        df_plot = df_plot.loc[start_year:end_year]
```

### 2. Validación de Tipos de Datos

```python
# Verificar compatibilidad de unidades antes de graficar
def validate_column_compatibility(selected_columns, table_metadata):
    units = []
    for col in selected_columns:
        col_info = table_metadata.get(col, {})
        units.append(col_info.get('unit', 'unknown'))
    
    # Advertir si las unidades son muy diferentes
    if len(set(units)) > 2:
        return False, "Advertencia: Las columnas tienen unidades muy diferentes"
    return True, ""
```

### 3. Normalización de Datos

```python
# Opción para normalizar series con escalas muy diferentes
def normalize_series(df, method='index_100'):
    if method == 'index_100':
        return df / df.iloc[0] * 100
    elif method == 'z_score':
        return (df - df.mean()) / df.std()
    return df
```

### 4. Interactividad Avanzada

```python
# Usar Plotly en lugar de matplotlib para gráficas interactivas
import plotly.graph_objects as go
import plotly.express as px

def create_interactive_plot(df, columns, title):
    fig = go.Figure()
    
    for col in columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[col],
            mode='lines',
            name=col,
            hovertemplate=f'{col}: %{{y}}<br>Año: %{{x}}<extra></extra>'
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Año",
        yaxis_title="Valores",
        hovermode='x unified'
    )
    
    return fig
```

---

## 📝 Resumen de Componentes

| Componente | ID | Propósito | Tipo |
|------------|----|-----------| -----|
| table-selector | Dropdown | Seleccionar tabla de BD | Input |
| table-details-panel | Div | Mostrar info de tabla | Output |
| year-range-container | Div | Contener RangeSlider | Output |
| year-range-slider | RangeSlider | Filtrar años | State |
| columns-selector | Dropdown | Seleccionar columnas | State |
| chart-title | Input | Título personalizado | State |
| generate-button | Button | Disparar generación | Input |
| status-message | Div | Mensajes de estado | Output |
| chart-container | Div | Mostrar gráfica | Output |

---

## 🎯 Conclusión

Este sistema implementa un **generador de gráficas interactivo** que:

1. **Carga dinámicamente** tablas desde SQLite
2. **Extrae metadata** desde archivos YAML
3. **Genera interfaces** adaptadas a cada tabla
4. **Crea gráficas** con estilo corporativo consistente
5. **Maneja errores** graciosamente
6. **Proporciona feedback** visual constante

La arquitectura modular permite **fácil extensión** y **mantenimiento**, mientras que el uso de Dash provides una **experiencia de usuario fluida** similar a aplicaciones web modernas.

**La clave del éxito** está en la **separación de responsabilidades**: metadata en YAML, datos en SQLite, lógica en Python, y presentación en Dash components.
