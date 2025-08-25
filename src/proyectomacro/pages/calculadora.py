# src/proyectomacro/pages/calculadora.py
import dash
from dash import html, dcc, dash_table, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from datetime import datetime

from proyectomacro.extract_data import list_table_image_groups
from proyectomacro.page_utils import build_breadcrumb, build_header, build_data_table, load_metadata_from_config
from func_auxiliares.graficos_utils import get_df
from func_auxiliares.config import DB_PATH

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

dash.register_page(
    __name__,
    path="/calculadora",
    name="Calculadora",
    title="Calculadora Macroeconómica",
    metadata={"section": "Herramientas"},
)

# ────────────────────────────────────────────────────────────────────────
# Funciones auxiliares
# ────────────────────────────────────────────────────────────────────────

def get_available_tables():
    """Obtener lista de tablas disponibles en la base de datos"""
    try:
        # Obtener lista de tablas desde la base de datos
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        tables_df = get_df(query, conn_str=str(DB_PATH))
        return tables_df['name'].tolist()
    except Exception as e:
        print(f"Error obteniendo tablas: {e}")
        return []

def get_table_columns(table_name):
    """Obtener columnas de una tabla específica"""
    try:
        query = f"PRAGMA table_info({table_name})"
        columns_df = get_df(query, conn_str=str(DB_PATH))
        return columns_df['name'].tolist()
    except Exception as e:
        print(f"Error obteniendo columnas de {table_name}: {e}")
        return []

def calculate_growth_rates(df, column, method='anual', periods=1):
    """
    Calcular tasas de crecimiento para una serie temporal
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame con índice temporal
    column : str
        Nombre de la columna a calcular
    method : str
        Tipo de cálculo: 'anual', 'trimestral', 'acumulado'
    periods : int
        Número de períodos para el cálculo
    
    Returns:
    --------
    pandas.Series
        Serie con las tasas de crecimiento calculadas
    """
    if column not in df.columns:
        return pd.Series(dtype=float)
    
    series = df[column].copy()
    
    if method == 'anual':
        # Tasa de crecimiento anual: (Vt / Vt-1) - 1
        growth_rate = series.pct_change(periods=periods) * 100
    elif method == 'trimestral':
        # Tasa de crecimiento trimestral
        growth_rate = series.pct_change(periods=periods) * 100
    elif method == 'acumulado':
        # Crecimiento acumulado desde el primer período
        first_value = series.iloc[0]
        growth_rate = ((series / first_value) - 1) * 100
    else:
        growth_rate = series.pct_change(periods=periods) * 100
    
    return growth_rate

def calculate_means(df, column, method='simple', window=None):
    """
    Calcular diferentes tipos de medias
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame con los datos
    column : str
        Columna a calcular
    method : str
        Tipo de media: 'simple', 'movil', 'ponderada'
    window : int
        Ventana para media móvil
    
    Returns:
    --------
    pandas.Series or float
        Media calculada
    """
    if column not in df.columns:
        return None
    
    series = df[column].dropna()
    
    if method == 'simple':
        return series.mean()
    elif method == 'movil' and window:
        return series.rolling(window=window).mean()
    elif method == 'ponderada':
        # Media ponderada por tiempo (más peso a datos recientes)
        weights = np.arange(1, len(series) + 1)
        return np.average(series, weights=weights)
    
    return series.mean()

# ────────────────────────────────────────────────────────────────────────
# Layout
# ────────────────────────────────────────────────────────────────────────

def layout(**kwargs):
    # Obtener tablas disponibles
    available_tables = get_available_tables()
    
    breadcrumb = build_breadcrumb(
        crumbs=[
            {"label": "Inicio", "href": "/"},
            {"label": "Calculadora Macroeconómica", "active": True}
        ],
        status="✅ Herramienta disponible",
        badge_success_marker="✅"
    )
    
    metadata = {
        "Descripción": "Herramienta para calcular tasas de crecimiento y medias de variables macroeconómicas",
        "Funcionalidades": [
            "Cálculo de tasas de crecimiento anuales, trimestrales y acumuladas",
            "Cálculo de medias simples, móviles y ponderadas", 
            "Análisis de períodos personalizados",
            "Visualización gráfica de resultados"
        ],
        "Uso": "Seleccione una tabla, columna y configure los parámetros de cálculo"
    }
    
    header = build_header(
        title="🧮 Calculadora Macroeconómica",
        desc="Herramienta para cálculos personalizados de tasas de crecimiento y medias estadísticas",
        metadata=metadata,
        toggle_id="calc-btn-toggle-meta",
        collapse_id="calc-meta-panel"
    )
    
    return html.Div([
        breadcrumb,
        html.Br(),
        header,
        html.Br(),
        
        # Panel de control principal
        dbc.Card([
            dbc.CardHeader([
                html.H4("⚙️ Panel de Control", className="mb-0")
            ]),
            dbc.CardBody([
                dbc.Row([
                    # Columna izquierda: Selección de datos
                    dbc.Col([
                        html.H5("📊 Selección de Datos"),
                        html.Hr(),
                        
                        # Selector de tabla
                        html.Label("Tabla:", className="fw-bold"),
                        dcc.Dropdown(
                            id="calc-table-dropdown",
                            options=[{"label": table, "value": table} for table in available_tables],
                            placeholder="Seleccione una tabla...",
                            className="mb-3"
                        ),
                        
                        # Selector de columna
                        html.Label("Variable:", className="fw-bold"),
                        dcc.Dropdown(
                            id="calc-column-dropdown",
                            placeholder="Primero seleccione una tabla...",
                            className="mb-3"
                        ),
                        
                        # Rango de años
                        html.Label("Rango de Años:", className="fw-bold"),
                        dcc.RangeSlider(
                            id="calc-year-range",
                            min=1950,
                            max=2025,
                            value=[2000, 2023],
                            marks={i: str(i) for i in range(1950, 2026, 10)},
                            tooltip={"placement": "bottom", "always_visible": True},
                            className="mb-3"
                        ),
                        
                    ], width=6),
                    
                    # Columna derecha: Configuración de cálculos
                    dbc.Col([
                        html.H5("🔧 Configuración de Cálculos"),
                        html.Hr(),
                        
                        # Sección Tasas de Crecimiento
                        html.H6("📈 Tasas de Crecimiento", className="text-primary"),
                        
                        html.Label("Tipo de Cálculo:", className="fw-bold"),
                        dcc.Dropdown(
                            id="calc-growth-method",
                            options=[
                                {"label": "Anual (año a año)", "value": "anual"},
                                {"label": "Trimestral", "value": "trimestral"},
                                {"label": "Acumulado (desde base)", "value": "acumulado"}
                            ],
                            value="anual",
                            className="mb-3"
                        ),
                        
                        html.Label("Períodos:", className="fw-bold"),
                        dbc.Input(
                            id="calc-growth-periods",
                            type="number",
                            value=1,
                            min=1,
                            max=10,
                            className="mb-3"
                        ),
                        
                        # Sección Medias
                        html.H6("📊 Cálculo de Medias", className="text-success"),
                        
                        html.Label("Tipo de Media:", className="fw-bold"),
                        dcc.Dropdown(
                            id="calc-mean-method",
                            options=[
                                {"label": "Media Simple", "value": "simple"},
                                {"label": "Media Móvil", "value": "movil"},
                                {"label": "Media Ponderada", "value": "ponderada"}
                            ],
                            value="simple",
                            className="mb-3"
                        ),
                        
                        html.Label("Ventana (para media móvil):", className="fw-bold"),
                        dbc.Input(
                            id="calc-mean-window",
                            type="number",
                            value=3,
                            min=2,
                            max=20,
                            disabled=True,
                            className="mb-3"
                        ),
                        
                    ], width=6),
                ])
            ])
        ], className="mb-4"),
        
        # Botones de acción
        dbc.Row([
            dbc.Col([
                dbc.ButtonGroup([
                    dbc.Button(
                        "🧮 Calcular",
                        id="calc-calculate-btn",
                        color="primary",
                        size="lg",
                        className="me-2"
                    ),
                    dbc.Button(
                        "🔄 Limpiar",
                        id="calc-clear-btn",
                        color="secondary",
                        outline=True,
                        size="lg",
                        className="me-2"
                    ),
                    dbc.Button(
                        "📊 Graficar",
                        id="calc-plot-btn",
                        color="info",
                        outline=True,
                        size="lg",
                        disabled=True
                    )
                ], className="mb-4")
            ], width=12, className="text-center")
        ]),
        
        # Área de resultados
        html.Div(id="calc-results-area"),
        
        # Área de gráficos
        html.Div(id="calc-plots-area"),
        
        # Store para datos calculados
        dcc.Store(id="calc-data-store"),
        
    ])

# ────────────────────────────────────────────────────────────────────────
# Callbacks
# ────────────────────────────────────────────────────────────────────────

@callback(
    Output("calc-meta-panel", "is_open"),
    Input("calc-btn-toggle-meta", "n_clicks"),
    State("calc-meta-panel", "is_open"),
    prevent_initial_call=True,
)
def toggle_meta(n_clicks, is_open):
    return not is_open

@callback(
    Output("calc-column-dropdown", "options"),
    Output("calc-column-dropdown", "value"),
    Input("calc-table-dropdown", "value"),
    prevent_initial_call=True
)
def update_column_options(selected_table):
    if not selected_table:
        return [], None
    
    columns = get_table_columns(selected_table)
    # Filtrar columnas numéricas típicas (excluir año que suele ser índice)
    numeric_columns = [col for col in columns if col.lower() not in ['año', 'year', 'fecha', 'date']]
    
    options = [{"label": col, "value": col} for col in numeric_columns]
    return options, None

@callback(
    Output("calc-mean-window", "disabled"),
    Input("calc-mean-method", "value"),
    prevent_initial_call=True
)
def toggle_mean_window(mean_method):
    return mean_method != "movil"

@callback(
    Output("calc-results-area", "children"),
    Output("calc-data-store", "data"),
    Output("calc-plot-btn", "disabled"),
    Input("calc-calculate-btn", "n_clicks"),
    State("calc-table-dropdown", "value"),
    State("calc-column-dropdown", "value"),
    State("calc-year-range", "value"),
    State("calc-growth-method", "value"),
    State("calc-growth-periods", "value"),
    State("calc-mean-method", "value"),
    State("calc-mean-window", "value"),
    prevent_initial_call=True
)
def calculate_results(n_clicks, table, column, year_range, growth_method, growth_periods, mean_method, mean_window):
    if not n_clicks or not table or not column:
        return html.Div(), {}, True
    
    try:
        # Cargar datos
        query = f"SELECT * FROM {table}"
        df = get_df(query, conn_str=str(DB_PATH))
        
        # Filtrar por años si hay columna año
        if 'año' in df.columns:
            df = df.set_index('año')
            df = df.loc[year_range[0]:year_range[1]]
        
        if column not in df.columns:
            return dbc.Alert("Columna no encontrada en la tabla.", color="danger"), {}, True
        
        # Calcular tasas de crecimiento
        growth_rates = calculate_growth_rates(df, column, growth_method, growth_periods)
        
        # Calcular medias
        if mean_method == "movil":
            mean_result = calculate_means(df, column, mean_method, mean_window)
        else:
            mean_result = calculate_means(df, column, mean_method)
        
        # Preparar resultados
        results_df = pd.DataFrame({
            'Año': df.index,
            f'{column}': df[column],
            f'Tasa_Crecimiento_{growth_method}': growth_rates
        })
        
        if isinstance(mean_result, pd.Series):
            results_df[f'Media_{mean_method}'] = mean_result
        
        # Estadísticas resumen
        stats = {
            'Media Original': df[column].mean(),
            'Desviación Estándar': df[column].std(),
            'Mínimo': df[column].min(),
            'Máximo': df[column].max(),
            'Tasa Crecimiento Promedio': growth_rates.mean(),
            'Tasa Crecimiento Máxima': growth_rates.max(),
            'Tasa Crecimiento Mínima': growth_rates.min()
        }
        
        if isinstance(mean_result, (int, float)):
            stats[f'Media {mean_method}'] = mean_result
        
        # Crear cards con resultados
        results_content = [
            # Card de estadísticas
            dbc.Card([
                dbc.CardHeader([
                    html.H5("📊 Estadísticas Resumen", className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.P([
                                html.Strong(f"{key}: "),
                                f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
                            ]) for key, value in list(stats.items())[:4]
                        ], width=6),
                        dbc.Col([
                            html.P([
                                html.Strong(f"{key}: "),
                                f"{value:.2f}%" if 'Tasa' in key and isinstance(value, (int, float)) else 
                                f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
                            ]) for key, value in list(stats.items())[4:]
                        ], width=6)
                    ])
                ])
            ], className="mb-4"),
            
            # Card de tabla de resultados
            dbc.Card([
                dbc.CardHeader([
                    html.H5("📋 Resultados Detallados", className="mb-0")
                ]),
                dbc.CardBody([
                    build_data_table(
                        results_df.set_index('Año'),
                        "calc-results",
                        page_size=15
                    )
                ])
            ])
        ]
        
        # Preparar datos para store
        store_data = {
            'table': table,
            'column': column,
            'results_df': results_df.to_dict('records'),
            'stats': stats,
            'year_range': year_range
        }
        
        return results_content, store_data, False
        
    except Exception as e:
        error_msg = f"Error en el cálculo: {str(e)}"
        return dbc.Alert(error_msg, color="danger"), {}, True

@callback(
    Output("calc-plots-area", "children"),
    Input("calc-plot-btn", "n_clicks"),
    State("calc-data-store", "data"),
    prevent_initial_call=True
)
def create_plots(n_clicks, stored_data):
    if not n_clicks or not stored_data:
        return html.Div()
    
    try:
        # Reconstruir DataFrame
        results_df = pd.DataFrame(stored_data['results_df'])
        column = stored_data['column']
        
        # Crear gráficos con subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                f'Serie Original: {column}',
                'Tasas de Crecimiento',
                'Media Móvil (si aplica)',
                'Distribución de Tasas'
            ],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Gráfico 1: Serie original
        fig.add_trace(
            go.Scatter(
                x=results_df['Año'],
                y=results_df[column],
                mode='lines+markers',
                name=column,
                line=dict(color='blue', width=2)
            ),
            row=1, col=1
        )
        
        # Gráfico 2: Tasas de crecimiento
        growth_col = [col for col in results_df.columns if 'Tasa_Crecimiento' in col][0]
        fig.add_trace(
            go.Scatter(
                x=results_df['Año'],
                y=results_df[growth_col],
                mode='lines+markers',
                name='Tasa de Crecimiento',
                line=dict(color='red', width=2)
            ),
            row=1, col=2
        )
        
        # Gráfico 3: Media móvil si existe
        media_cols = [col for col in results_df.columns if 'Media_' in col]
        if media_cols:
            fig.add_trace(
                go.Scatter(
                    x=results_df['Año'],
                    y=results_df[media_cols[0]],
                    mode='lines',
                    name='Media Calculada',
                    line=dict(color='green', width=2)
                ),
                row=2, col=1
            )
        
        # Gráfico 4: Histograma de tasas
        fig.add_trace(
            go.Histogram(
                x=results_df[growth_col].dropna(),
                name='Distribución Tasas',
                marker_color='orange',
                opacity=0.7
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=800,
            showlegend=True,
            title_text=f"Análisis Completo: {column}",
            title_x=0.5
        )
        
        # Actualizar ejes usando update_layout
        fig.update_layout(
            xaxis_title="Año",
            xaxis2_title="Año", 
            xaxis3_title="Año",
            xaxis4_title="Tasa de Crecimiento (%)",
            yaxis_title=column,
            yaxis2_title="Tasa (%)",
            yaxis3_title="Media",
            yaxis4_title="Frecuencia"
        )
        
        return dbc.Card([
            dbc.CardHeader([
                html.H5("📈 Análisis Gráfico", className="mb-0")
            ]),
            dbc.CardBody([
                dcc.Graph(figure=fig, config={'displayModeBar': True})
            ])
        ], className="mt-4")
        
    except Exception as e:
        return dbc.Alert(f"Error creando gráficos: {str(e)}", color="danger")

@callback(
    Output("calc-table-dropdown", "value"),
    Output("calc-column-dropdown", "value", allow_duplicate=True),
    Output("calc-results-area", "children", allow_duplicate=True),
    Output("calc-plots-area", "children", allow_duplicate=True),
    Input("calc-clear-btn", "n_clicks"),
    prevent_initial_call=True
)
def clear_calculator(n_clicks):
    if n_clicks:
        return None, None, html.Div(), html.Div()
    return no_update, no_update, no_update, no_update
