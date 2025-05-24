from dash import dcc, html, dash_table
from config import tab_style, tab_selected_style, table_styles
import dash_bootstrap_components as dbc

# Función que genera los tabs para los periodos de un mineral
def create_period_tabs_for_mineral_generic(series_file, period_file, base_path):
    """
    Crea un conjunto de tabs para los periodos de un mineral.
    Parámetros:
      - series_file: nombre del archivo para Serie Completa.
      - period_file: nombre del archivo para los demás periodos.
      - base_path: ruta base a la carpeta donde se encuentran las imágenes.
    """
    periods = [
        ("Serie Completa", "serie_completa", series_file),
        ("1952–1982", "periodo_1952-1982", period_file),
        ("1982–2006", "periodo_1982-2006", period_file),
        ("2006–2025", "periodo_2006-2025", period_file)
    ]
    period_tabs = []
    for label, folder, file in periods:
        period_tabs.append(
            dcc.Tab(
                label=label,
                style=tab_style,
                selected_style=tab_selected_style,
                children=[
                    html.Div(
                        html.Img(
                            src=f"{base_path}{folder}/{file}",
                            style={"width": "80%", "height": "auto"}
                        ),
                        className="d-flex justify-content-center"
                    )
                ]
            )
        )
    return dcc.Tabs(children=period_tabs)
# ----------------------------- 
# TABS DE MINERALES
# -----------------------------
def create_mineral_tab_generic(mineral_label, series_file, period_file, base_path):
    """
    Crea un tab para un mineral, incorporando los tabs de periodos.
    Parámetros:
      - mineral_label: etiqueta del mineral (p.ej. "Estaño").
      - series_file: nombre del archivo para la serie completa.
      - period_file: nombre del archivo para los periodos.
      - base_path: ruta base a la carpeta (volumen o valor).
    """
    return dcc.Tab(
        label=mineral_label,
        style=tab_style,
        selected_style=tab_selected_style,
        children=[create_period_tabs_for_mineral_generic(series_file, period_file, base_path)]
    )
# Función para crear tarjetas (cards) con cada tabla
def create_table_card(title, dataframe):
    return dbc.Card(
        dbc.CardBody([
            html.H4(title, className="card-title text-center"),
            dash_table.DataTable(
                data=dataframe.to_dict('records'),
                columns=[{"name": col, "id": col} for col in dataframe.columns],
                page_size=15,
                **table_styles
            )
        ]),
        className="mb-4 shadow"
    )
def is_safe_query(sql_query):
    """
    Verifica que la consulta SQL solo contenga comandos de lectura (SELECT).
    Retorna True si es segura, False si no lo es.
    """
    sql_query = sql_query.lower().strip()
    return sql_query.startswith("select") and not any(
        forbidden in sql_query for forbidden in ["drop", "delete", "update", "insert", "alter"]
    )
# ----------------------------- 
# ESTADISTICAS DESCRIPTIVAS POR PERIODOS
# -----------------------------
def create_descriptive_stats_table(df, title):
    """
    Genera una tarjeta que contiene una tabla de estadísticas descriptivas (df.describe())
    del DataFrame df, con un título dado.
    """
    # Calcular estadísticas y redondear
    stats_df = df.describe().round(2).reset_index()
    return dbc.Card(
        dbc.CardBody([
            html.H4(title, className="card-title text-center"),
            dash_table.DataTable(
                data=stats_df.to_dict('records'),
                columns=[{"name": col, "id": col} for col in stats_df.columns],
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'center', 'padding': '5px'},
                style_header={'backgroundColor': '#007BFF', 'fontWeight': 'bold', 'color': 'white'}
            )
        ]),
        className="mb-4 shadow"
    )

def create_period_descriptive_stats_tabs(df, periods, title_prefix):
    """
    Genera un conjunto de tabs, uno por cada periodo, donde se muestran las estadísticas descriptivas del DataFrame df.
    
    Parámetros:
      - df: DataFrame con los datos (se asume que su índice es el año)
      - periods: lista de tuplas (label, start, end) donde 'end' puede ser None para indicar hasta el final.
      - title_prefix: Texto base para el título, por ejemplo, "Estadísticas Descriptivas - Balanza Comercial"
    
    Retorna:
      - dcc.Tabs con un tab para cada periodo.
    """
    period_tabs = []
    for label, start, end in periods:
        # Filtrar el DataFrame por el periodo. Si end es None, se toma desde start hasta el final.
        if end is None:
            df_period = df.loc[df.index >= start]
        else:
            df_period = df.loc[(df.index >= start) & (df.index < end)]
        
        # Crear la tarjeta de estadísticas para ese periodo
        card = create_descriptive_stats_table(df_period, f"{title_prefix} ({label})")
        
        period_tabs.append(
            dcc.Tab(
                label=label,
                style=tab_style,
                selected_style=tab_selected_style,
                children=[card]
            )
        )
    return dcc.Tabs(children=period_tabs)