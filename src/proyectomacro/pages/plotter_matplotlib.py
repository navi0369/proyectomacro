"""
Página para generar gráficas personalizadas con matplotlib
Solo líneas simples, sin anotaciones ni elementos adicionales
"""
import dash
from dash import html, dcc, Input, Output, State, callback
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo para servidor
import io
import base64
import sqlite3
import yaml
import os
import re

from proyectomacro.extract_data import load_validated_tables
from func_auxiliares.config import DB_PATH
from func_auxiliares.graficos_utils import set_style, get_df, init_base_plot

dash.register_page(
    __name__,
    path="/plotter-matplotlib",
    name="Generador de Gráficas",
    title="Generador de Gráficas de Serie Completa",
    description="Genera gráficas de líneas simples usando matplotlib",
)

# Obtener lista de tablas disponibles
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

def get_table_columns(table_name):
    """Obtener columnas de una tabla específica"""
    try:
        query = f"PRAGMA table_info({table_name})"
        columns_df = get_df(query, conn_str=str(DB_PATH))
        return columns_df['name'].tolist()
    except Exception as e:
        print(f"Error obteniendo columnas de {table_name}: {e}")
        return []

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

def matplotlib_to_base64(fig):
    """Convierte figura matplotlib a string base64 para mostrar en Dash"""
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close(fig)  # Importante: cerrar figura para liberar memoria
    return f"data:image/png;base64,{image_base64}"

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

# Layout de la página
layout = html.Div([
    html.Div([
        html.H3("Generador de Gráficas de Serie Completa", 
                style={'text-align': 'center', 'color': '#2E4B8A', 'margin-bottom': '30px'}),
        
        # Selector de tabla
        html.Div([
            html.Label("Seleccionar Tabla:", style={'font-weight': 'bold', 'margin-bottom': '10px'}),
            dcc.Dropdown(
                id='table-selector',
                options=[{'label': table, 'value': table} for table in get_available_tables()],
                placeholder="Selecciona una tabla...",
                style={'margin-bottom': '20px'}
            )
        ]),
        
        # Panel de detalles de la tabla (se muestra cuando se selecciona una tabla)
        html.Div(
            id='table-details-panel',
            style={'margin-bottom': '20px'}
        ),
        
        # Selector de rango de años
        html.Div(
            id='year-range-container',
            style={'margin-bottom': '20px'}
        ),
        
        # Selector de columnas
        html.Div([
            html.Label("Seleccionar Columnas (máximo 5):", style={'font-weight': 'bold', 'margin-bottom': '10px'}),
            dcc.Dropdown(
                id='columns-selector',
                multi=True,
                placeholder="Primero selecciona una tabla...",
                style={'margin-bottom': '20px'}
            )
        ]),
        
        # Título personalizado
        html.Div([
            html.Label("Título de la Gráfica:", style={'font-weight': 'bold', 'margin-bottom': '10px'}),
            dcc.Input(
                id='chart-title',
                type='text',
                placeholder="Título personalizado (opcional)",
                style={'width': '100%', 'padding': '8px', 'margin-bottom': '20px'}
            )
        ]),
        
        # Botón para generar
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
        ], style={'text-align': 'center'}),
        
        # Mensaje de estado
        html.Div(id='status-message', style={'margin-bottom': '20px'}),
        
        # Contenedor para la gráfica
        html.Div(id='chart-container', style={'text-align': 'center'})
        
    ], style={
        'max-width': '1200px',
        'margin': '0 auto',
        'padding': '20px',
        'background-color': '#f8f9fa',
        'border-radius': '10px',
        'box-shadow': '0 2px 10px rgba(0,0,0,0.1)'
    })
])

# Callback para actualizar opciones de columnas cuando se selecciona una tabla
@callback(
    Output('columns-selector', 'options'),
    Output('columns-selector', 'value'),
    Input('table-selector', 'value'),
    prevent_initial_call=True
)
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

# Callback para generar el selector de rango de años
@callback(
    Output('year-range-container', 'children'),
    Input('table-selector', 'value'),
    prevent_initial_call=True
)
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

# Callback para mostrar detalles de la tabla seleccionada
@callback(
    Output('table-details-panel', 'children'),
    Input('table-selector', 'value'),
    prevent_initial_call=True
)
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

# Callback principal para generar la gráfica
@callback(
    Output('chart-container', 'children'),
    Output('status-message', 'children'),
    Input('generate-button', 'n_clicks'),
    State('table-selector', 'value'),
    State('columns-selector', 'value'),
    State('chart-title', 'value')
)
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
        
        # Generar título
        if custom_title:
            title = custom_title
        else:
            title = f"{selected_table} - {', '.join(selected_columns[:3])}"
            if len(selected_columns) > 3:
                title += "..."
        
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
        
    except Exception as e:
        error_msg = html.Div(
            f"❌ Error generando gráfica: {str(e)}",
            style={'color': 'red'}
        )
        return [], error_msg
