import os
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import re
import pandas as pd
import matplotlib.pyplot as plt
from graficas import create_line_plot, fig_to_base64 
from openai import OpenAI
import sqlite3

from config import DB_PATH, MODEL_NAME, OPENAI_API_KEY, PERIODOS, table_styles, tabs_styles, tab_style, tab_selected_style, minerals_volumen_info, minerals_valor_info, volumen_base, valor_base

from llm_utils import generate_sql_from_question, generate_explanation
from functions import create_period_tabs_for_mineral_generic, create_mineral_tab_generic, create_table_card, is_safe_query, create_period_descriptive_stats_tabs



os.chdir(os.path.dirname(os.path.abspath(__file__)))

# -----------------------------
# Configuración y Conexión a la Base de Datos Macroeconómica
# ----------------------------- 
conn = sqlite3.connect("file:db/proyectomacro.db?mode=ro", uri=True)
cursor = conn.cursor()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# -----------------------------
# Cargar Datos en DataFrames
# -----------------------------
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
_TABLE_NAMES = [row[0] for row in cursor.fetchall()]

# Diccionario con todos los DataFrames disponibles
dfs = {name: pd.read_sql(f"SELECT * FROM {name}", conn) for name in _TABLE_NAMES}

# Variables de uso común para compatibilidad con el código previo
df_pib = dfs.get("PIB_Real_Gasto")
df_tasa = dfs.get("Tasa_Crecimiento_PIB")
df_precio_oficial = dfs.get("precio_oficial_minerales")
df_produccion = dfs.get("produccion_minerales")
df_precio = dfs.get("precio_minerales")
df_balanza = dfs.get("balanza_comercial")
df_participacion = dfs.get("Participacion_PIB")
df_reservas = dfs.get("Reservas_oro_divisas")
df_exp_trad_no_trad = dfs.get("participacion_exp_trad_no_trad")
df_grado_de_apertura = dfs.get("grado_de_apertura")
df_participacion_x_m_pib = dfs.get("participacion_x_m_pib")
df_composicion_importaciones_uso_destino = dfs.get("composicion_importaciones_uso_destino")
df_exportaciones_totales = dfs.get("exportaciones_totales")
df_participacion_composicion_importaciones_uso_destino = dfs.get("participacion_composicion_importaciones_uso_destino")
df_participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos = dfs.get("participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos")
df_participacion_hidrocarburos_minerales_exportaciones_tradicionales = dfs.get("participacion_hidrocarburos_minerales_exportaciones_tradicionales")
df_exportacion_gas_natural = dfs.get("exportacion_gas_natural")
df_exportacion_gas_natural_contratos = dfs.get("exportacion_gas_natural_contratos")
df_exportaciones_minerales_totales = dfs.get("exportaciones_minerales_totales")
df_operaciones_empresas_publicas = dfs.get("operaciones_empresas_publicas")
df_balanza_de_pagos = dfs.get("balanza_de_pagos")
df_consolidado_spnf = dfs.get("consolidado_spnf")
df_deuda_externa_total = dfs.get("deuda_externa_total")
df_deuda_interna = dfs.get("deuda_interna")
df_inversion_publica_por_sectores = dfs.get("inversion_publica_por_sectores")
df_inversion_publica_total = dfs.get("inversion_publica_total")
df_exportaciones_tradicionales_no_tradicionales = dfs.get("exportaciones_tradicionales_no_tradicionales")
df_flujo_divisas = dfs.get("flujo_divisas")
df_pib_ramas = dfs.get("pib_ramas")
df_exportaciones_tradicionales_hidrocarburos = dfs.get("exportaciones_tradicionales_hidrocarburos")
df_exportaciones_tradicionales = dfs.get("exportaciones_tradicionales")
df_participacion_pib_ramas = dfs.get("participacion_pib_ramas")
df_exportaciones_no_tradicionales = dfs.get("exportaciones_no_tradicionales")
df_exportaciones_por_pais_de_destino = dfs.get("exportaciones_por_pais_de_destino")
df_inflacion_acumulada = dfs.get("inflacion_acumulada")
df_inflacion_general_acumulada = dfs.get("inflacion_general_acumulada")
df_cotizacion_oficial_dolar = dfs.get("cotizacion_oficial_dolar")
df_mercado_laboral = dfs.get("mercado_laboral")
df_pib_nominal_gasto = dfs.get("pib_nominal_gasto")
df_deflactor_implicito_pib_gasto = dfs.get("deflactor_implicito_pib_gasto")
df_oferta_total = dfs.get("oferta_total")
df_demanda_total = dfs.get("demanda_total")
df_vbp_sector_2006_2014 = dfs.get("vbp_sector_2006_2014")
df_ingresos_nacionales = dfs.get("ingresos_nacionales")
df_pobreza = dfs.get("pobreza")
df_pobreza_extrema = dfs.get("pobreza_extrema")
df_precio_petroleo_wti = dfs.get("precio_petroleo_wti")
df_fuente_tablas = dfs.get("fuente_tablas")

# Utilidades para construir las tabs de la nueva interfaz
def table_tab(label, table_key):
    df = dfs.get(table_key)
    content = dbc.Container(create_table_card(label, df), fluid=True) if df is not None else html.Div("Datos no disponibles")
    return dcc.Tab(label=label, style=tab_style, selected_style=tab_selected_style, children=[content])

def create_main_layout():
    return dbc.Container([
        html.H1("Dashboard de Datos Macroeconómicos y Asistente IA", className="text-center my-4 text-primary", style={"fontFamily": "Arial, sans-serif"}),
        dcc.Tabs(style=tabs_styles, children=[
            dcc.Tab(label="Cuentas Nacionales / PIB", style=tab_style, selected_style=tab_selected_style, children=[
                table_tab("Desagregación del PIB por ramas de actividad", "pib_ramas"),
                table_tab("Participación de exportaciones e importaciones en el PIB", "participacion_x_m_pib"),
                table_tab("Tasa de crecimiento anual del PIB", "Tasa_Crecimiento_PIB"),
                table_tab("Participación del PIB por ramas de actividad", "participacion_pib_ramas"),
                table_tab("PIB a precios corrientes por tipo de gasto", "pib_nominal_gasto"),
                table_tab("Deflactor implícito del PIB por tipo de gasto", "deflactor_implicito_pib_gasto"),
                table_tab("Oferta total y componentes", "oferta_total"),
                table_tab("Demanda total y componentes", "demanda_total"),
                table_tab("VBP por ramas de actividad económica", "vbp_sector_2006_2014")
            ]),
            dcc.Tab(label="Sector Externo / Balanza Comercial", style=tab_style, selected_style=tab_selected_style, children=[
                table_tab("Flujo de Divisas del Sector Externo", "flujo_divisas"),
                table_tab("Grado de Apertura Económica", "grado_de_apertura"),
                table_tab("Reservas Internacionales de Oro y Divisas", "Reservas_oro_divisas")
            ]),
            dcc.Tab(label="Exportaciones", style=tab_style, selected_style=tab_selected_style, children=[
                table_tab("Exportaciones Totales", "exportaciones_totales"),
                table_tab("Volumen y Valor de Exportaciones de Minerales", "exportaciones_minerales_totales"),
                table_tab("Exportaciones Tradicionales", "exportaciones_tradicionales"),
                table_tab("Exportaciones Tradicionales y No Tradicionales", "exportaciones_tradicionales_no_tradicionales"),
                table_tab("Participación de exportaciones tradicionales y no tradicionales", "participacion_exp_trad_no_trad"),
                table_tab("Exportaciones tradicionales de hidrocarburos", "exportaciones_tradicionales_hidrocarburos"),
                table_tab("Exportación de Gas Natural", "exportacion_gas_natural"),
                table_tab("Exportación de Gas Natural por Contrato", "exportacion_gas_natural_contratos"),
                table_tab("Participación del Gas Natural y Otros Hidrocarburos en exportaciones de hidrocarburos", "participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos"),
                table_tab("Participación hidrocarburos vs minerales en exportaciones tradicionales", "participacion_hidrocarburos_minerales_exportaciones_tradicionales")
            ]),
            dcc.Tab(label="Importaciones", style=tab_style, selected_style=tab_selected_style, children=[
                table_tab("Composición de importaciones por uso y destino", "composicion_importaciones_uso_destino"),
                table_tab("Participación de la composición de importaciones por uso y destino", "participacion_composicion_importaciones_uso_destino"),
                table_tab("Exportaciones No Tradicionales", "exportaciones_no_tradicionales")
            ]),
            dcc.Tab(label="Precios y Producción", style=tab_style, selected_style=tab_selected_style, children=[
                table_tab("Precio real de minerales", "precio_minerales"),
                table_tab("Precios oficiales de minerales principales", "precio_oficial_minerales"),
                table_tab("Precio internacional del petróleo WTI", "precio_petroleo_wti"),
                table_tab("Producción de minerales principales", "produccion_minerales"),
                table_tab("Inflación acumulada", "inflacion_acumulada"),
                table_tab("Cotización oficial del dólar", "cotizacion_oficial_dolar")
            ]),
            dcc.Tab(label="Sector Fiscal", style=tab_style, selected_style=tab_selected_style, children=[
                table_tab("Consolidado de operaciones del SPNF", "consolidado_spnf"),
                table_tab("Operaciones de empresas públicas", "operaciones_empresas_publicas"),
                table_tab("Inversión pública total", "inversion_publica_total"),
                table_tab("Inversión pública por sectores", "inversion_publica_por_sectores"),
                table_tab("Ingresos Nacionales", "ingresos_nacionales")
            ]),
            dcc.Tab(label="Deuda", style=tab_style, selected_style=tab_selected_style, children=[
                table_tab("Deuda externa total", "deuda_externa_total"),
                table_tab("Deuda interna pública", "deuda_interna")
            ]),
            dcc.Tab(label="Empleo", style=tab_style, selected_style=tab_selected_style, children=[
                table_tab("Mercado laboral", "mercado_laboral")
            ]),
            dcc.Tab(label="Asistente IA", style=tab_style, selected_style=tab_selected_style, children=[
                dbc.Container([
                    html.H3("Asistente de Consultas Macroeconómicas", className="text-center my-4 text-secondary"),
                    dbc.Row([
                        dbc.Col(
                            dcc.Textarea(
                                id="input_pregunta",
                                placeholder=("Escribe tu consulta en lenguaje natural, por ejemplo:\n"
                                             "- ¿Cuál fue el crecimiento del PIB en 2020?\n"
                                             "- Muéstrame el gasto en consumo y formación de capital para el año 2015."),
                                style={
                                    "width": "100%",
                                    "height": "120px",
                                    "borderRadius": "5px",
                                    "padding": "10px",
                                    "fontFamily": "Arial, sans-serif",
                                    "fontSize": "14px"
                                }
                            ), md=8
                        )
                    ], className="mb-3 justify-content-center"),
                    dbc.Row([
                        dbc.Col(
                            dbc.Button("Consultar", id="btn_consultar", color="primary", size="lg", n_clicks=0),
                            width="auto", className="text-center"
                        )
                    ], className="mb-3 justify-content-center"),
                    dbc.Row([
                        dbc.Col(
                            html.Div(id="output_respuesta",
                                     style={
                                         "white-space": "pre-line",
                                         "border": "1px solid #ddd",
                                         "padding": "15px",
                                         "borderRadius": "5px",
                                         "backgroundColor": "#f8f9fa",
                                         "fontFamily": "Arial, sans-serif",
                                         "fontSize": "14px"
                                     }),
                            md=10
                        )
                    ], className="justify-content-center")
                ], fluid=True)
            ])
        ])
    ], fluid=True, style={"backgroundColor": "#e9ecef", "padding": "20px"})
# -----------------------------
# GRAFICAS
# -----------------------------
# Definir parámetros para anotaciones y áreas
annotate_bottom = [1953, 1956, 1959, 1967, 1974, 1982, 1986, 1992, 1999, 2009, 2020, 2024]
annotate_top = [1951, 1955, 1958, 1960, 1966, 1968, 1991, 2008, 2013, 2021]
fill_areas = [
    {'start': 1951, 'end': 1956, 'color': 'mistyrose', 'alpha': 0.7, 'label': "1951-1956"},
    {'start': 1957, 'end': 1970, 'color': 'lightgreen', 'alpha': 0.4, 'label': "1957-1970"},
    {'start': 1971, 'end': 1981, 'color': 'mistyrose', 'alpha': 0.7, 'label': "1971-1981"},
    {'start': 1982, 'end': 1986, 'color': 'mistyrose', 'alpha': 0.7, 'label': "1982-1986"},
    {'start': 1987, 'end': 2005, 'color': 'lightgreen', 'alpha': 0.4, 'label': "1987-2005"},
    {'start': 2006, 'end': 2014, 'color': 'lightgreen', 'alpha': 0.4, 'label': "2006-2014"},
    {'start': 2015, 'end': 2025, 'color': 'mistyrose', 'alpha': 0.7, 'label': "2015-2025"},
]
# Calcular las anotaciones de medias (ejemplo)
annotations = []
for period in fill_areas:
    start, end = period["start"], period["end"]
    mask = (df_tasa["año"] >= start) & (df_tasa["año"] <= end)
    period_mean = df_tasa.loc[mask, "crecimiento"].mean()
    mean_year = (start + end) // 2
    annotations.append({
        "x": mean_year,
        "y": -7.5,
        "text": f"Media: {period_mean:.2f}%",
        "va": "bottom" if period_mean > 0 else "top",
        "ha": "center",
        "fontsize": 12,
        "color": "red"
    })

# Generar la gráfica con la función importada
fig, ax = create_line_plot(
    df=df_tasa,
    y_col='crecimiento',
    title="Tasa de Crecimiento del PIB con Media por Período",
    xlabel="año",
    ylabel="Tasa de Crecimiento",
    annotations=annotations,
    x_col='año',
    annotate_bottom_years=annotate_bottom,
    annotate_top_years=annotate_top,
    fill_ranges=fill_areas,
    line_options={'marker': 'o', 'color': 'steelblue', 'linestyle': '-', 'linewidth': 2}
)
# 📌 Mostrar solo años de dos en dos
tick_years = df_tasa["año"].iloc[::2]  
ax.set_xticks(tick_years)
# Convertir la figura a imagen Base64
image_base64 = fig_to_base64(fig) 

# ----------------------------- 
# ESTADISTICAS DESCRIPTIVAS
# -----------------------------
estadisticas_pib = create_period_descriptive_stats_tabs(
    df = df_pib.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - PIB Real Gasto"
)

estadisticas_tasa = create_period_descriptive_stats_tabs(
    df = df_tasa.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Tasa de Crecimiento del PIB"
)

estadisticas_precio_oficial = create_period_descriptive_stats_tabs(
    df = df_precio_oficial.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Precio Oficial de Minerales"
)

estadisticas_produccion = create_period_descriptive_stats_tabs(
    df = df_produccion.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Producción de Minerales"
)

estadisticas_precio = create_period_descriptive_stats_tabs(
    df = df_precio.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Precio de Minerales"
)

estadisticas_balanza = create_period_descriptive_stats_tabs(
    df = df_balanza.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Balanza Comercial"
)

estadisticas_participacion = create_period_descriptive_stats_tabs(
    df = df_participacion.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Participación en el PIB"
)

estadisticas_reservas = create_period_descriptive_stats_tabs(
    df = df_reservas.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Reservas de Oro y Divisas"
)

estadisticas_exp_trad = create_period_descriptive_stats_tabs(
    df = df_exp_trad_no_trad.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Exportaciones Tradicionales vs No Tradicionales"
)

estadisticas_grado_de_apertura = create_period_descriptive_stats_tabs(
    df = df_grado_de_apertura.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Grado de Apertura"
)

estadisticas_participacion_x_m_pib= create_period_descriptive_stats_tabs(
    df = df_participacion_x_m_pib.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Participación X/M PIB"
)

estadisticas_composicion_importaciones_uso_destino = create_period_descriptive_stats_tabs(
    df = df_composicion_importaciones_uso_destino.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Composición de Importaciones Uso Destino"
)

estadisticas_exportaciones = create_period_descriptive_stats_tabs(
    df = df_exportaciones_totales.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Exportaciones Totales"
) 

estadisticas_participacion_composicion_importaciones_uso_destino= create_period_descriptive_stats_tabs(
    df = df_participacion_composicion_importaciones_uso_destino.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Participación en Importaciones Uso Destino"
)

estadisticas_participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos = create_period_descriptive_stats_tabs(
    df = df_participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Participación Gas en Hidrocarburos"
)

estadisticas_participacion_hidrocarburos_minerales_exportaciones_tradicionales = create_period_descriptive_stats_tabs(
    df = df_participacion_hidrocarburos_minerales_exportaciones_tradicionales.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Participación Hidrocarburos y Minerales"
)

estadisticas_gas_natural = create_period_descriptive_stats_tabs(
    df = df_exportacion_gas_natural.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Exportación de Gas Natural"
)

estadisticas_gas_natural_contratos = create_period_descriptive_stats_tabs(
    df = df_exportacion_gas_natural_contratos.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Exportación de Gas Natural por Contratos"
)

estadisticas_exportaciones_minerales_totales = create_period_descriptive_stats_tabs(
    df = df_exportaciones_minerales_totales.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Exportaciones de Minerales Valor y Cantidad"
)

estadisticas_operaciones_empresas_publicas = create_period_descriptive_stats_tabs(
    df = df_operaciones_empresas_publicas.set_index("año"),
    periods = PERIODOS,
    title_prefix = "Estadísticas Descriptivas - Operaciones Empresas Publicas"
)

# ----------------------------- 
# TABS DE MINERALES
# -----------------------------
# Generar tabs para cada mineral (volumen)
volumen_mineral_tabs = [
    create_mineral_tab_generic(label, series_file, period_file, volumen_base)
    for label, series_file, period_file in minerals_volumen_info
]


# Generar tabs para cada mineral (valor)
valor_mineral_tabs = [
    create_mineral_tab_generic(label, series_file, period_file, valor_base)
    for label, series_file, period_file in minerals_valor_info
]

# -----------------------------
# Configuración del Dashboard con Dash y Bootstrap
# -----------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

old_layout = dbc.Container([
    html.H1("Dashboard de Datos Macroeconómicos y Asistente IA", 
            className="text-center my-4 text-primary", 
            style={"fontFamily": "Arial, sans-serif"}),
    dcc.Tabs(
        style=tabs_styles,
        children=[
            # Tab para indicadores del PIB y Crecimiento
            dcc.Tab(
                label="PIB y Crecimiento",
                style=tab_style,
                selected_style=tab_selected_style,
                children=[
                    #GRAFICAS DEL PIB
                    dcc.Tabs(
                        children=[
                            #PIB REAL GASTO
                            dcc.Tab(
                                label="PIB Real Gasto",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("PIB Real Gasto", df_pib), fluid=True),
                                    dbc.Container(estadisticas_pib, fluid=True),
                                    #grafica de componentes y pib
                                    dcc.Tabs(
                                        id='nested-graph-tabs',
                                        children=[
                                            #PIB Real Base 1990
                                            dcc.Tab(
                                                label='PIB Real Base 1990',
                                                children=[
                                                    html.Div(
                                                        html.Img(src='/assets/imagenes/3.pib_real_gasto/serie_completa/3.pib_real_base_1990.png',
                                                                style={"width": "80%", "height": "auto"}),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            #Gastos Consumo
                                            dcc.Tab(
                                                label='Gastos Consumo',
                                                children=[
                                                    html.Div(
                                                        html.Img(src='../assets/imagenes/3.pib_real_gasto/serie_completa/3.1gastos_consumo.png',
                                                                style={"width": "80%", "height": "auto"}),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            #Formacion Capital
                                            dcc.Tab(
                                                label='Formacion Capital',
                                                children=[
                                                    html.Div(
                                                        html.Img(src='../assets/imagenes/3.pib_real_gasto/serie_completa/3.2formacion_capital.png',
                                                                style={"width": "80%", "height": "auto"}),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            #Exportacion Bienes Servicios
                                            dcc.Tab(
                                                label='Exportacion Bienes Servicios',
                                                children=[
                                                    html.Div(
                                                        html.Img(src='../assets/imagenes/3.pib_real_gasto/serie_completa/3.3exportacion_bienes_servicios.png',
                                                                style={"width": "80%", "height": "auto"}),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            #Importacion Bienes
                                            dcc.Tab(
                                                label='Importacion Bienes',
                                                children=[
                                                    html.Div(
                                                        html.Img(src='../assets/imagenes/3.pib_real_gasto/serie_completa/3.4importacion_bienes.png',
                                                                style={"width": "80%", "height": "auto"}),
                                                        className="d-flex justify-content-center"
                                                    )
                                            
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            #Consumo Privado
                                            dcc.Tab(
                                                label='consumo privado',
                                                children=[
                                                    html.Div(
                                                        html.Img(src='../assets/imagenes/3.pib_real_gasto/serie_completa/3.5consumo_privado.png',
                                                                style={"width": "80%", "height": "auto"}),
                                                        className="d-flex justify-content-center"
                                                    )
                                            
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            #Consumo Publico
                                            dcc.Tab(
                                                label='consumo',
                                                children=[
                                                    html.Div(
                                                        html.Img(src='../assets/imagenes/3.pib_real_gasto/serie_completa/3.6consumo_publico.png',
                                                                style={"width": "80%", "height": "auto"}),
                                                        className="d-flex justify-content-center"
                                                    )
                                            
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            )
                                        ]
                                    ),
                                    dcc.Markdown('''
                                        # 📊 **PIB por Tipo de Gasto (Miles de Bolivianos de 1990)**  

                                        ## 📌 **Descripción de la Tabla `PIB_Real_Gasto`**  
                                        Esta tabla almacena la descomposición del **PIB real** basado en el gasto de la economía, expresado en **miles de bolivianos constantes de 1990**.  

                                        ### 📄 **Estructura de la Tabla**  

                                        | **Columna**                     | **Descripción**                                                    | **Unidad**                 |
                                        |--------------------------------|----------------------------------------------------------------|--------------------------|
                                        | `Año`                          | Año del registro                                              | Año                      |
                                        | `Gastos_Consumo`               | Gasto total en consumo (privado y público)                   | Miles de bolivianos 1990 |
                                        | `Formacion_Capital`            | Inversión en formación bruta de capital fijo                 | Miles de bolivianos 1990 |
                                        | `Exportacion_Bienes_Servicios` | Valor total de exportaciones de bienes y servicios           | Miles de bolivianos 1990 |
                                        | `Importacion_Bienes`           | Valor total de importaciones de bienes y servicios           | Miles de bolivianos 1990 |
                                        | `PIB_Real_Base_1990`           | PIB real ajustado a precios constantes de 1990               | Miles de bolivianos 1990 |

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** 👉 [INE - Producto Interno Bruto](https://www.ine.gob.bo/index.php/estadisticas-economicas/pib-y-cuentas-nacionales/producto-interno-bruto-anual/serie-historica-del-producto-interno-bruto/)  

                                        📌 **Valores ajustados a precios constantes de 1990** para eliminar efectos de la inflación.  
                                        📅 **Frecuencia:** Datos anuales disponibles hasta el año más reciente registrado.  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            ),
                            #PARTICIPACION EN EL PIB
                            #esta tabla hay que eliminarla ya que la tabla participacion_x_m_pib es la misma
                            dcc.Tab(
                                label="Participación en X-M en PIB",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Participación en el PIB", df_participacion), fluid=True),
                                    dbc.Container(estadisticas_participacion, fluid=True),
                                    html.Img(src='/assets/imagenes/2.png', style={'width': '100%'}),
                                    dbc.Container(create_table_card("Estadísticos - Participación de Exportaciones e Importaciones en el PIB (%)", df_participacion.drop(columns=["año"]).describe().round(2).reset_index()), fluid=True),
                                    dcc.Markdown('''
                                        # 📊 **Participación de Exportaciones e Importaciones en el PIB (%)**  

                                        ## 📌 **Descripción de la Tabla `participacion_x_m_pib`**  
                                        Esta tabla mide qué porcentaje del **PIB** está representado por **exportaciones e importaciones**, con las siguientes fórmulas:

                                        📌 **X/PIB (%) = Exportaciones / PIB**  
                                        📌 **M/PIB (%) = Importaciones / PIB**  

                                        ### 📄 **Columnas**  

                                        | **Columna**  | **Descripción**                               | **Unidad**     |
                                        |-------------|---------------------------------------------|--------------|
                                        | `Año`       | Año del registro                          | Año         |
                                        | `X`         | Exportaciones como % del PIB              | Porcentaje  |
                                        | `M`         | Importaciones como % del PIB              | Porcentaje  |

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** 👉 [INE - Macroeconomía](https://www.ine.gob.bo)  
                                        📅 **Frecuencia:** Datos anuales.  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            ),
                            #TASA DE CRECIMIENTO
                            dcc.Tab(
                                label="Tasa Crecimiento PIB",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Tasa_Crecimiento_PIB", df_tasa), fluid=True),
                                    dbc.Container(estadisticas_tasa, fluid=True),   
                                    dcc.Markdown('''
                                        # 📈 **Tasa de Crecimiento del PIB (%)**  

                                        ## 📌 **Descripción de la Tabla `tasa_crecimiento_pib`**  
                                        Esta tabla muestra la evolución del **crecimiento del Producto Interno Bruto (PIB) real** respecto al año anterior, expresado en porcentaje.

                                        ### 📄 **Columnas**  

                                        | **Columna**      | **Descripción**                                         | **Unidad**       |
                                        |-----------------|---------------------------------------------------------|----------------|
                                        | `Año`          | Año del registro                                        | Año           |
                                        | `Crecimiento`  | Tasa de crecimiento del PIB real (%)                     | Porcentaje    |

                                        📌 **Ejemplo:** Si el valor es `4.5`, significa que el PIB creció **4.5%** con respecto al año anterior.

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** 👉 [Instituto Nacional de Estadística (INE)](https://www.ine.gob.bo)  
                                        📅 **Frecuencia:** Datos anuales.  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"}),
                                        
                                        html.Div([
                                            html.Img(src=image_base64, style={"width": "100%", "height": "auto"})
                                        ], className="d-flex justify-content-center")
                                ]
                            )
                        ]
                    )
                ]
            ),
            # Tab para Precios y Producción de Minerales
            dcc.Tab(
                label="Precios y Producción",
                style=tab_style,
                selected_style=tab_selected_style,
                children=[
                    dcc.Tabs(
                        children=[
                            #PRECIO OFICIAL MINERALES
                            dcc.Tab(
                                label="Precio Oficial Minerales",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Precio Oficial Minerales", df_precio_oficial), fluid=True),
                                    dbc.Container(estadisticas_precio_oficial, fluid=True),
                                    dcc.Tabs(
                                        id='nested-minerals-tabs',
                                        children=[
                                            dcc.Tab(
                                                label='Zinc',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/4.precio_oficial_minerales/4.1.zinc.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Estaño',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/4.precio_oficial_minerales/4.2.estano.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Oro',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/4.precio_oficial_minerales/4.3.oro.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Plata',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/4.precio_oficial_minerales/4.4.plata.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Antimonio',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/4.precio_oficial_minerales/4.5.antimonio.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Plomo',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/4.precio_oficial_minerales/4.6.plomo.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Wolfram',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/4.precio_oficial_minerales/4.7.wolfram.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Cobre',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/4.precio_oficial_minerales/4.8.cobre.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Bismuto',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/4.precio_oficial_minerales/4.9.bismuto.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Cadmio',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/4.precio_oficial_minerales/4.10.cadmio.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Manganeso',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/4.precio_oficial_minerales/4.11.manganeso.png',
                                                            style={"width": "100%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            )
                                        ]),
                                    dcc.Markdown('''
                                        # 💰 **Precios de Minerales (Dólares Americanos de 1990)**  

                                        ## 📌 **Descripción de las Tablas `precio_minerales` y `precio_oficial_minerales`**  
                                        Estas tablas almacenan los precios históricos de distintos minerales en dólares ajustados al valor de **1990**.  

                                        ### 📄 **Estructura de la Tabla**  

                                        | **Columna**   | **Descripción**                                    | **Unidad**              |
                                        |--------------|------------------------------------------------|-----------------------|
                                        | `Año`       | Año del registro                              | Año                   |
                                        | `Zinc`      | Precio del Zinc (Libras Finas - L.F)         | USD                   |
                                        | `Estaño`    | Precio del Estaño (Libras Finas - L.F)       | USD                   |
                                        | `Oro`       | Precio del Oro (Onzas Troy - O.T.)          | USD                   |
                                        | `Plata`     | Precio de la Plata (Onzas Troy - O.T.)      | USD                   |
                                        | `Antimonio` | Precio del Antimonio (Toneladas Métricas)   | USD                   |
                                        | `Plomo`     | Precio del Plomo (Libras Finas - L.F)       | USD                   |
                                        | `Wólfram`   | Precio del Wólfram (Unidades Libras Finas)  | USD                   |
                                        | `Cobre`     | Precio del Cobre (Libras Finas - L.F)       | USD                   |

                                        📌 **Unidades de Medida**  
                                        - **L.F. (Libras Finas)** → Zinc, Estaño, Plomo y Cobre.  
                                        - **O.T. (Onzas Troy)** → Oro y Plata.  
                                        - **T.M.F. (Toneladas Métricas Finas)** → Antimonio.  
                                        - **U.L.F. (Unidades Libras Finas)** → Wólfram.  

                                        ## ⚠️ **Notas**  
                                        🔗 **Fuente:** 👉 [Informe Oficial](https://mineria.gob.bo/revista/pdf/20170817-10-15-28.pdf)  
                                        📌 **Valores en USD ajustados a 1990**.  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            ),
                            #PRECIO MINERAL (REAL)
                            dcc.Tab(
                                label="Precio Minerales (Reales)",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Precio Minerales (Reales)", df_precio), fluid=True),
                                    dbc.Container(estadisticas_precio, fluid=True),
                                    dcc.Markdown('''
                                        # 💰 **Precios de Minerales (Dólares Americanos de 1990)**  

                                        ## 📌 **Descripción de las Tablas `precio_minerales` y `precio_oficial_minerales`**  
                                        Estas tablas almacenan los precios históricos de distintos minerales en dólares ajustados al valor de **1990**.  

                                        ### 📄 **Estructura de la Tabla**  

                                        | **Columna**   | **Descripción**                                    | **Unidad**              |
                                        |--------------|------------------------------------------------|-----------------------|
                                        | `Año`       | Año del registro                              | Año                   |
                                        | `Zinc`      | Precio del Zinc (Libras Finas - L.F)         | USD                   |
                                        | `Estaño`    | Precio del Estaño (Libras Finas - L.F)       | USD                   |
                                        | `Oro`       | Precio del Oro (Onzas Troy - O.T.)          | USD                   |
                                        | `Plata`     | Precio de la Plata (Onzas Troy - O.T.)      | USD                   |
                                        | `Antimonio` | Precio del Antimonio (Toneladas Métricas)   | USD                   |
                                        | `Plomo`     | Precio del Plomo (Libras Finas - L.F)       | USD                   |
                                        | `Wólfram`   | Precio del Wólfram (Unidades Libras Finas)  | USD                   |
                                        | `Cobre`     | Precio del Cobre (Libras Finas - L.F)       | USD                   |

                                        📌 **Unidades de Medida**  
                                        - **L.F. (Libras Finas)** → Zinc, Estaño, Plomo y Cobre.  
                                        - **O.T. (Onzas Troy)** → Oro y Plata.  
                                        - **T.M.F. (Toneladas Métricas Finas)** → Antimonio.  
                                        - **U.L.F. (Unidades Libras Finas)** → Wólfram.  

                                        ## ⚠️ **Notas**  
                                        🔗 **Fuente:** 👉 [Informe Oficial](https://mineria.gob.bo/revista/pdf/20170817-10-15-28.pdf)  
                                        📌 **Valores en USD ajustados a 1990**.  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            ),
                            #PRODUCCION MINERALES
                            dcc.Tab(
                                label="Producción de Minerales",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Producción de Minerales", df_produccion), fluid=True),
                                    dbc.Container(estadisticas_produccion, fluid=True),
                                    dcc.Tabs(
                                        id='minerales-tabs',
                                        children=[
                                            dcc.Tab(
                                                label='Zinc',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/9.produccion_minerales/9.1.zinc.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Estaño',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/9.produccion_minerales/9.2.estaño.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Oro',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/9.produccion_minerales/9.3.oro.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Plata',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/9.produccion_minerales/9.4.plata.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Antimonio',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/9.produccion_minerales/9.5.antimonio.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Plomo',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/9.produccion_minerales/9.6.plomo.png',
                                                            style={"width": "100%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Wólfram',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/9.produccion_minerales/9.7.wolfram.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Cobre',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/9.produccion_minerales/9.8.cobre.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                        ]
                                    ),
                                    dcc.Markdown('''
                                        # 📊 **Producción de Minerales (Toneladas Finas)**  

                                        ## 📌 **Descripción de la Tabla `produccion_minerales`**  
                                        Esta tabla almacena la producción anual de minerales en toneladas finas desde **1985 hasta 2021**.  

                                        ### 📄 **Columnas**  

                                        | **Columna**   | **Descripción**                      | **Unidad**         |
                                        |--------------|------------------------------------|------------------|
                                        | `Año`       | Año de la producción minera       | Año              |
                                        | `Zinc`      | Producción de zinc                | Toneladas finas  |
                                        | `Estaño`    | Producción de estaño              | Toneladas finas  |
                                        | `Oro`       | Producción de oro                 | Toneladas finas  |
                                        | `Plata`     | Producción de plata               | Toneladas finas  |
                                        | `Antimonio` | Producción de antimonio           | Toneladas finas  |
                                        | `Plomo`     | Producción de plomo               | Toneladas finas  |
                                        | `Wólfram`   | Producción de wólfram             | Toneladas finas  |
                                        | `Cobre`     | Producción de cobre               | Toneladas finas  |

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** Datos obtenidos del Ministerio de Minería de Bolivia.  
                                        👉 [Descargar Informe Oficial](https://mineria.gob.bo/revista/pdf/20170817-10-15-28.pdf)  

                                        📅 **Frecuencia:** Datos anuales desde **1985 hasta 2021**.  
                                        📐 **Formato:** Los valores están en **toneladas finas**.  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            )
                        ]
                    )
                ]
            ),
            # Tab para Comercio Exterior
            dcc.Tab(
                label="Comercio Exterior",
                style=tab_style,
                selected_style=tab_selected_style,
                children=[
                    dcc.Tabs(
                        children=[
                            #BALANZA COMERCIAL
                            dcc.Tab(
                                label="Balanza Comercial",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Balanza Comercial", df_balanza), fluid=True),
                                    dbc.Container(estadisticas_balanza, fluid=True),
                                    html.Img(
                                                            src='/assets/imagenes/7.balanza_comercial/7.1_balanza_comercial.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                    dcc.Markdown('''
                                        # 💰 **Balanza Comercial (Millones de USD)**  

                                        ## 📌 **Descripción de la Tabla `balanza_comercial`**  
                                        Esta tabla muestra los valores anuales de **exportaciones e importaciones**, así como el saldo comercial, en **millones de dólares estadounidenses**.

                                        ### 📄 **Columnas**  

                                        | **Columna**       | **Descripción**                             | **Unidad**          |
                                        |------------------|-----------------------------------------|-------------------|
                                        | `Año`           | Año del registro                        | Año              |
                                        | `Exportaciones` | Valor total de exportaciones           | Millones de USD  |
                                        | `Importaciones` | Valor total de importaciones           | Millones de USD  |
                                        | `Saldo_Comercial` | Diferencia entre exportaciones e importaciones | Millones de USD  |

                                        📌 **Saldo Comercial = Exportaciones - Importaciones**  
                                        Si el saldo es **positivo**, el país tiene **superávit** comercial.  
                                        Si es **negativo**, el país tiene **déficit** comercial.

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** 👉 [INE - Balanza Comercial](https://www.ine.gob.bo)  
                                        📅 **Frecuencia:** Datos anuales.  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            ),
                            #EXPORTACIONES TOTALES
                            dcc.Tab(
                                label="Exportaciones Totales",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Exportaciones Totales", df_exportaciones_totales), fluid=True),
                                    dbc.Container(estadisticas_exportaciones, fluid=True),
                                    dcc.Tabs(
                                        id='nested-exportaciones-tabs',
                                        children=[
                                            #Evolución Total
                                            dcc.Tab(
                                                label='Evolución Total',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/5.exportaciones_totales/5.1_evolucion_valor_total.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            #Exportaciones Tradicionales vs No Tradicionales
                                            dcc.Tab(
                                                label='Tradicional vs No Tradicional',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/5.exportaciones_totales/5.2_exportaciones_tradicionales_vs_no_tradicionales.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            #Barras Apiladas
                                            dcc.Tab(
                                                label='Barras Apiladas',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/5.exportaciones_totales/5.3_exportaciones_stacked_bar.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            #Porcentajes
                                            dcc.Tab(
                                                label='Porcentajes',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/5.exportaciones_totales/5.4_porcentaje_exportaciones.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            #Distribución y Relaciones
                                            dcc.Tab(
                                                label='Distribución y Relaciones',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/5.exportaciones_totales/5.5_distribucion_pairplot.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            )
                                        ]
                                    ),
                                    dcc.Markdown('''
                                        # 🚢 **Exportaciones Totales (Millones de USD)**  

                                        ## 📌 **Descripción de la Tabla `exportaciones_totales`**  
                                        Esta tabla detalla las **exportaciones tradicionales y no tradicionales** del país, expresadas en **millones de dólares**.

                                        ### 📄 **Columnas**  

                                        | **Columna**                 | **Descripción**                                      | **Unidad**       |
                                        |----------------------------|--------------------------------------------------|----------------|
                                        | `Año`                      | Año del registro                               | Año           |
                                        | `Productos_Tradicionales`  | Exportación de minerales y productos agroindustriales | Millones de USD  |
                                        | `Productos_No_Tradicionales` | Exportación de productos industriales y manufacturados | Millones de USD  |
                                        | `Total_Valor_Oficial`      | Total exportado (Tradicionales + No Tradicionales) | Millones de USD  |

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** 👉 [INE - Comercio Exterior](https://www.ine.gob.bo)  
                                        📅 **Frecuencia:** Datos anuales.  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            ),
                            #EXPORTACIONES TRADICIONALES VS NO TRADICIONALES
                            dcc.Tab(
                                label="Exp Trad vs No Trad",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Exp Trad vs No Trad", df_exp_trad_no_trad), fluid=True),
                                    dbc.Container(estadisticas_exp_trad, fluid=True),
                                    dcc.Markdown('''
                                        # 📊 **Participación de Exportaciones Tradicionales y No Tradicionales (%)**  

                                        ## 📌 **Descripción de la Tabla `exp_trad_no_trad`**  
                                        Esta tabla muestra la proporción de **exportaciones tradicionales** y **no tradicionales** como porcentaje del total de exportaciones.

                                        ### 📄 **Columnas**  

                                        | **Columna**   | **Descripción**                                               | **Unidad**    |
                                        |--------------|---------------------------------------------------------------|--------------|
                                        | `Año`       | Año del registro                                              | Año         |
                                        | `exp_trad`  | Exportaciones Tradicionales (% del total)                      | Porcentaje  |
                                        | `exp_no_trad` | Exportaciones No Tradicionales (% del total)                 | Porcentaje  |

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** 👉 [INE - Instituto Nacional de Estadística](https://www.ine.gob.bo)  
                                        📅 **Frecuencia:** Datos anuales.  
                                        📊 **Definición:**  
                                        - **Exportaciones Tradicionales**: Incluyen productos primarios como minerales, hidrocarburos y productos agroindustriales básicos.  
                                        - **Exportaciones No Tradicionales**: Comprenden productos manufacturados, agroindustria avanzada y otros bienes con mayor valor agregado.  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            ),
                            #EXPORTACIONES DE GAS NATURAL
                            dcc.Tab(
                                label="Exportaciones de gas natural",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Exportaciones de gas natural", df_exportacion_gas_natural), fluid=True),
                                    dbc.Container(estadisticas_gas_natural, fluid=True),
                                    dcc.Tabs(
                                        id='exportaciones-gas-natural-tabs',
                                        children=[
                                            #Evolución del Monto
                                            dcc.Tab(
                                                label='Evolución del Monto',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/10.exportaciones_gas_natural/10.1_evolucion_del_monto.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            #Evolución de Cantidades
                                            dcc.Tab(
                                                label='Evolución de Cantidades',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/10.exportaciones_gas_natural/10.2_evolucion_de_cantidades.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            #Evolución Monto y Cantidades   
                                            dcc.Tab(
                                                label='Evolución Monto y Cantidades',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/10.exportaciones_gas_natural/10.3_evolucion_de_monto_y_cantidades.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Evolución de precios',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/10.exportaciones_gas_natural/10.4_evolucion_de_precios.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            )
                                        ]
                                    ),
                                    dcc.Markdown('''
                                        # 🌐 **Exportaciones de Gas Natural (1992–2024)**  

                                        ## 📌 **Descripción de la Tabla `exportacion_gas_natural`**  
                                        Esta tabla contiene los datos de exportación de **gas natural** de Bolivia desde el año 1992 hasta 2024, expresados en **millones de dólares estadounidenses**, **toneladas métricas** y el **precio promedio por MPC**.

                                        ### 📄 **Columnas**  

                                        | **Columna**   | **Descripción**                             | **Unidad**             |
                                        |--------------|---------------------------------------------|------------------------|
                                        | `año`        | Año del registro                             | Año                    |
                                        | `monto`      | Valor de exportación de gas natural          | Millones de USD        |
                                        | `toneladas`  | Volumen exportado de gas natural             | Peso neto (Toneladas)  |
                                        | `precio`     | Precio promedio de exportación de gas        | USD/MPC                |

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** 👉 [INE - Instituto Nacional de Estadística (descargar datos)](https://nube.ine.gob.bo/index.php/s/zUQc65wIGkw1KUy/download)  
                                        📅 **Frecuencia:** Datos anuales.  

                                        📊 **Definición:**  
                                        - **Exportaciones de gas natural**: Incluyen ventas externas de gas natural por ductos, considerando precios internacionales y volúmenes entregados.  
                                        - **Precio ($us/MPC)**: Valor promedio por mil pies cúbicos exportados en el año correspondiente.
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            ),
                            #VALOR DE LAS EXPORTACIONES DE GAS NATURAL POR CONTRATOS
                            dcc.Tab(
                                label="Exportaciones de gas natural por contratos",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Exportaciones de gas natural por contratos",df_exportacion_gas_natural_contratos), fluid=True),
                                    dbc.Container(estadisticas_gas_natural_contratos, fluid=True),
                                    dcc.Tabs(
                                        id='exportacion-gas-natural-contratos-tabs',
                                        children=[
                                            dcc.Tab(
                                                label='Evolución por Destino',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/11.exportacion_gas_natural_contratos/11.2_evolucion_por_destino.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            ),
                                            dcc.Tab(
                                                label='Distribución por Contrato',
                                                children=[
                                                    html.Div(
                                                        html.Img(
                                                            src='/assets/imagenes/11.exportacion_gas_natural_contratos/11.3_distribucion_por_contrato_multiline.png',
                                                            style={"width": "80%", "height": "auto"}
                                                        ),
                                                        className="d-flex justify-content-center"
                                                    )
                                                ],
                                                style=tab_style,
                                                selected_style=tab_selected_style
                                            )
                                        ]
                                    ),
                                    dcc.Markdown('''
                                        # 📄 **Valor de Exportación de Gas Natural por Contrato (1992–2023)**

                                        ## 📌 **Descripción de la Tabla `exportacion_gas_natural_contratos`**  
                                        Esta tabla desglosa el valor anual de las **exportaciones de gas natural** de Bolivia, clasificado por contrato y país de destino (Argentina o Brasil), expresado en millones de dólares estadounidenses.

                                        ### 📄 **Columnas**  

                                        | **Columna**   | **Descripción**                                                  | **Unidad**           |
                                        |---------------|------------------------------------------------------------------|----------------------|
                                        | `año`         | Año del registro                                                 | Año                  |
                                        | `contrato`    | Nombre del contrato de exportación firmado por YPFB             | Texto                |
                                        | `destino`     | País de destino del gas exportado (Argentina o Brasil)          | Texto                |
                                        | `monto`       | Valor exportado bajo ese contrato en el año correspondiente     | Millones de USD      |

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** 👉 [INE - Instituto Nacional de Estadística (descargar datos)](https://dossier.udape.gob.bo/res/VALOR%20DE%20EXPORTACI%C3%93N%20DE%20GAS%20NATURAL%20POR%20CONTRATO)  
                                        📅 **Frecuencia:** Datos anuales.  
                                        📊 **Definición:**  
                                        - Incluye contratos bilaterales de exportación firmados por YPFB con empresas e instituciones en Argentina y Brasil.  
                                        - Los montos están expresados en millones de dólares y reflejan el valor comercial anual bajo cada contrato.  
                                        - Algunos contratos pueden no registrar exportaciones en ciertos años (omitidos si el valor es cero).
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})

                                ]
                            ),
                            #EXPORTACIONES DE MINERALES
                            dcc.Tab(
                                label="exportaciones de minerales",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Exportaciones de minerales valor y cantidad",df_exportaciones_minerales_totales), fluid=True),
                                    dbc.Container(estadisticas_exportaciones_minerales_totales, fluid=True),
                                    #VOLUMEN EXPORTADO DE MINERALES
                                    dcc.Tab(
                                        label="Volumen Exportado de Minerales",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=[
                                            dcc.Tabs(children=volumen_mineral_tabs)
                                        ]
                                    ),
                                    #VALOR EXPORTADO DE MINERALES
                                    dcc.Tab(
                                    label="Valor Exportado de Minerales",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                    children=[ dcc.Tabs(children=valor_mineral_tabs) ]
                                ),
                                    dcc.Markdown('''
                                        # 🪨 **Exportaciones de Minerales de Bolivia (1952–2023)**

                                        ## 📌 **Descripción de la Tabla `exportaciones_minerales_totales`**  
                                        Esta tabla contiene los datos anuales consolidados de **volumen** (en toneladas métricas finas) y **valor** (en miles de dólares) de exportación de los principales minerales bolivianos entre 1987 y 2023.

                                        ### 📄 **Columnas**  

                                        | **Columna**            | **Descripción**                             | **Unidad**                  |
                                        |------------------------|---------------------------------------------|-----------------------------|
                                        | `año`                | Año del registro                            | Año                         |
                                        | `estaño_volumen`      | Volumen exportado de estaño                 | kilos finos |
                                        | `estaño_valor`        | Valor exportado de estaño                   | Miles de USD               |
                                        | `plomo_volumen`       | Volumen exportado de plomo                  | kilos finos   |
                                        | `plomo_valor`         | Valor exportado de plomo                    | Miles de USD               |
                                        | `zinc_volumen`        | Volumen exportado de zinc                   | kilos finos  |
                                        | `zinc_valor`          | Valor exportado de zinc                     | Miles de USD               |
                                        | `plata_volumen`       | Volumen exportado de plata                  | kilos finos  |
                                        | `plata_valor`         | Valor exportado de plata                    | Miles de USD               |
                                        | `wolfram_volumen`     | Volumen exportado de wolfram                | kilos finos   |
                                        | `wolfram_valor`       | Valor exportado de wolfram                  | Miles de USD               |
                                        | `cobre_volumen`       | Volumen exportado de cobre                  | kilos finos   |
                                        | `cobre_valor`         | Valor exportado de cobre                    | Miles de USD               |
                                        | `antimonio_volumen`   | Volumen exportado de antimonio              | kilos finos  |
                                        | `antimonio_valor`     | Valor exportado de antimonio                | Miles de USD               |
                                        | `oro_volumen`         | Volumen exportado de oro                    | kilos finos   |
                                        | `oro_valor`           | Valor exportado de oro                      | Miles de USD               |

                                        ## 📌 **Notas**
                                        🔗 **Fuente oficial:** 👉 [UDAPE – Volumen y Valor de Exportaciones de Minerales](https://dossier.udape.gob.bo/res/VOLUMEN%20Y%20VALOR%20DE%20EXPORTACIONES%20DE%20MINERALES)
                                        
                                        🔗 **Fuente:** 👉 informes del banco central de bolivia.
                                        
                                        📅 **Frecuencia:** Datos anuales.
                                        📊 **Definición:**  
                                        - **Volumen**: Cantidad física exportada, expresada en kilos finos.  
                                        - **Valor**: Monto monetario de las exportaciones, expresado en miles de dólares estadounidenses (USD).
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            )
                        ]
                    )
                ]
            ),
            # Tab para Importaciones y Apertura Comercial
            dcc.Tab(
                label="Importaciones y Apertura",
                style=tab_style,
                selected_style=tab_selected_style,
                children=[
                    dcc.Tabs(
                        children=[
                            #composicion importaciones uso destino
                            dcc.Tab(
                                label="Composición Importaciones Uso Destino",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Composición Importaciones Uso Destino", df_composicion_importaciones_uso_destino), fluid=True),
                                    dbc.Container(estadisticas_composicion_importaciones_uso_destino, fluid=True),
                                    dcc.Markdown('''
                                        # 📊 **Composición de Importaciones según Uso o Destino Económico (Millones de USD)**  

                                        ## 📌 **Descripción de la Tabla `composicion_importaciones_uso_destino`**  
                                        Esta tabla detalla la composición de **importaciones** según su uso económico, desglosadas en bienes de consumo, materias primas, bienes de capital y otras importaciones.

                                        ### 📄 **Columnas**  

                                        | **Columna**                                     | **Descripción**                                        | **Unidad**             |
                                        |------------------------------------------------|--------------------------------------------------------|-----------------------|
                                        | `Año`                                         | Año del registro                                      | Año                  |
                                        | `Bienes_Consumo`                               | Importaciones de bienes de consumo                    | Millones de USD (CIF) |
                                        | `Materias_Primas_Productos_Intermedios`        | Importaciones de materias primas y productos intermedios | Millones de USD (CIF) |
                                        | `Bienes_Capital`                               | Importaciones de bienes de capital                    | Millones de USD (CIF) |
                                        | `Diversos`                                     | Otras importaciones                                  | Millones de USD (CIF) |
                                        | `Total_Valor_Oficial_CIF`                      | Total de importaciones CIF                           | Millones de USD       |

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** 👉 [INE - Instituto Nacional de Estadística](https://www.ine.gob.bo)  
                                        📅 **Frecuencia:** Datos anuales.  
                                        📊 **Observación:**  
                                        - **Desde 2016, los datos son preliminares.**  
                                        - **CIF (Cost, Insurance and Freight):** Incluye costo del producto, seguro y flete.  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            ),
                            #participacion composicion importaciones
                            dcc.Tab(
                                label="Participación Composición Importaciones",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Participación Composición Importaciones", df_participacion_composicion_importaciones_uso_destino), fluid=True),
                                    dbc.Container(estadisticas_participacion_composicion_importaciones_uso_destino, fluid=True),
                                    dcc.Markdown('''
                                        # 📊 **Composición de Importaciones según Uso o Destino Económico (%)**  

                                        ## 📌 **Descripción de la Tabla `composicion_importaciones_uso_destino_porcentaje`**  
                                        Esta tabla expresa la **participación relativa (%)** de cada categoría de importaciones dentro del **total importado**.

                                        ### 📄 **Columnas**  

                                        | **Columna**                                   | **Descripción**                                        | **Unidad**    |
                                        |----------------------------------------------|--------------------------------------------------------|--------------|
                                        | `Año`                                       | Año del registro                                      | Año         |
                                        | `Bienes_Consumo`                             | % de bienes de consumo en importaciones totales      | Porcentaje  |
                                        | `Materias_Primas_Productos_Intermedios`      | % de materias primas y productos intermedios         | Porcentaje  |
                                        | `Bienes_Capital`                             | % de bienes de capital en importaciones totales      | Porcentaje  |
                                        | `Diversos`                                   | % de otras importaciones no categorizadas            | Porcentaje  |
                                        | `Total_CIF`                                  | Total CIF (Siempre es 100%)                          | Porcentaje  |

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** 👉 [INE - Instituto Nacional de Estadística](https://www.ine.gob.bo)  
                                        📅 **Frecuencia:** Datos anuales.  
                                        📊 **Observación:**  
                                        - **Desde 2016, los datos son preliminares.**  
                                        - **Valores expresados como porcentaje del total CIF.**  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})

                                ]
                            ),
                            #Grado de apertura
                            dcc.Tab(
                                label="Grado de Apertura",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Grado de Apertura", df_grado_de_apertura), fluid=True),
                                    dbc.Container(estadisticas_grado_de_apertura, fluid=True),
                                    dcc.Markdown('''
                                        # 🌍 **Grado de Apertura Económica (%)**  

                                        ## 📌 **Descripción de la Tabla `grado_de_apertura`**  
                                        Esta tabla mide la **apertura económica** del país en términos del comercio exterior, calculado con la fórmula:

                                        📌 **Grado de Apertura = (Exportaciones + Importaciones) / PIB (%)**  

                                        ### 📄 **Columnas**  

                                        | **Columna**  | **Descripción**                                 | **Unidad**     |
                                        |-------------|-----------------------------------------------|--------------|
                                        | `Año`       | Año del registro                            | Año         |
                                        | `Grado`     | Nivel de apertura económica                | Porcentaje  |

                                        📌 **Valores Altos:** Indican mayor integración con el comercio internacional.  
                                        📌 **Valores Bajos:** Indican una economía más cerrada.  

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** 👉 [INE - Comercio Exterior](https://www.ine.gob.bo)  
                                        📅 **Frecuencia:** Datos anuales.  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            )
                        ]
                    )
                ]
            ),
            # Tab para Hidrocarburos y Minerales
            dcc.Tab(
                label="Hidrocarburos y Minerales",
                style=tab_style,
                selected_style=tab_selected_style,
                children=[
                    dcc.Tabs(
                        children=[
                            #PARTICIPACION GAS HIDROCARBUROS TOTAL EXPORTACIONES
                            dcc.Tab(
                                label="Participación Gas Hidrocarburos Total Exportaciones",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Participación Gas Hidrocarburos Total Exportaciones", df_participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos), fluid=True),
                                    dbc.Container(estadisticas_participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos, fluid=True),
                                    dcc.Markdown('''
                                        # 📊 **Participación del Gas en Exportaciones Totales de Hidrocarburos (%)**  

                                        ## 📌 **Descripción de la Tabla `participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos`**  
                                        Esta tabla mide la contribución del **gas natural** y otros hidrocarburos dentro del **total de exportaciones de hidrocarburos**.

                                        ### 📄 **Columnas**  

                                        | **Columna**         | **Descripción**                                      | **Unidad**    |
                                        |---------------------|------------------------------------------------------|--------------|
                                        | `Año`              | Año del registro                                     | Año         |
                                        | `Exportacion_Gas`  | Exportaciones de gas como % del total de hidrocarburos | Porcentaje  |
                                        | `Otros_Hidrocarburos` | Exportaciones de otros hidrocarburos como % del total | Porcentaje  |

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** 👉 [INE - Instituto Nacional de Estadística](https://www.ine.gob.bo)  
                                        📅 **Frecuencia:** Datos anuales.  
                                        📊 **Definición:**  
                                        - **Gas Natural**: Exportaciones de gas en relación al total de hidrocarburos.  
                                        - **Otros Hidrocarburos**: Petróleo y sus derivados dentro del total de exportaciones de hidrocarburos.  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            ),
                            #PARTICIPACION HIDROCARBUROS MINERALES TRADICIONALES
                            dcc.Tab(
                                label="Participación Hidrocarburos Minerales Tradicionales",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Participación Hidrocarburos Minerales Tradicionales", df_participacion_hidrocarburos_minerales_exportaciones_tradicionales), fluid=True),
                                    dbc.Container(estadisticas_participacion_hidrocarburos_minerales_exportaciones_tradicionales, fluid=True),
                                    dcc.Markdown('''
                                        # 📊 **Participación de Hidrocarburos y Minerales en Exportaciones Tradicionales (%)**  

                                        ## 📌 **Descripción de la Tabla `participacion_hidrocarburos_minerales_exportaciones_tradicionales`**  
                                        Esta tabla refleja el peso relativo de **minerales e hidrocarburos** dentro de las **exportaciones tradicionales** en diferentes años.

                                        ### 📄 **Columnas**  

                                        | **Columna**   | **Descripción**                                             | **Unidad**    |
                                        |--------------|-------------------------------------------------------------|--------------|
                                        | `Año`       | Año del registro                                            | Año         |
                                        | `Minerales` | Participación de los minerales en exportaciones tradicionales | Porcentaje  |
                                        | `Hidrocarburos` | Participación de los hidrocarburos en exportaciones tradicionales | Porcentaje  |

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** 👉 [INE - Instituto Nacional de Estadística](https://www.ine.gob.bo)  
                                        📅 **Frecuencia:** Datos anuales.  
                                        📊 **Definición:**  
                                        - **Minerales**: Incluyen oro, plata, zinc, estaño, plomo, cobre y otros.  
                                        - **Hidrocarburos**: Incluyen gas natural y otros derivados del petróleo.  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            ),
                            dcc.Tab(
                                label="Participación X/M PIB",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("Participación X/M PIB", df_participacion_x_m_pib), fluid=True),
                                    dbc.Container(estadisticas_participacion_x_m_pib, fluid=True),
                                    dcc.Markdown('''
                                        # 📊 **Participación de Exportaciones e Importaciones en el PIB (%)**  

                                        ## 📌 **Descripción de la Tabla `participacion_x_m_pib`**  
                                        Esta tabla mide qué porcentaje del **PIB** está representado por **exportaciones e importaciones**, con las siguientes fórmulas:

                                        📌 **X/PIB (%) = Exportaciones / PIB**  
                                        📌 **M/PIB (%) = Importaciones / PIB**  

                                        ### 📄 **Columnas**  

                                        | **Columna**  | **Descripción**                               | **Unidad**     |
                                        |-------------|---------------------------------------------|--------------|
                                        | `Año`       | Año del registro                          | Año         |
                                        | `X`         | Exportaciones como % del PIB              | Porcentaje  |
                                        | `M`         | Importaciones como % del PIB              | Porcentaje  |

                                        ## 📌 **Notas**  
                                        🔗 **Fuente:** 👉 [INE - Macroeconomía](https://www.ine.gob.bo)  
                                        📅 **Frecuencia:** Datos anuales.  
                                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            )
                        ]
                    )
                ]
            ),
            # Tab para Reservas
            dcc.Tab(
                label="Reservas",
                style=tab_style,
                selected_style=tab_selected_style,
                children=[
                    dbc.Container(create_table_card("Reservas de Oro y Divisas", df_reservas), fluid=True),
                    dbc.Container(estadisticas_reservas, fluid=True),
                    dcc.Markdown('''
                        # 📊 **Reservas de Oro y Divisas (Millones de USD)**  

                        ## 📌 **Descripción de la Tabla `Reservas_oro_divisas`**  
                        Esta tabla muestra la evolución de las **reservas internacionales de oro y divisas**, expresadas en **millones de dólares**.

                        ### 📄 **Columnas**  

                        | **Columna**        | **Descripción**                                   | **Unidad**        |
                        |-------------------|-------------------------------------------------|------------------|
                        | `Año`            | Año del registro                                | Año             |
                        | `Reservas_Totales` | Total de reservas de oro y divisas en el país  | Millones de USD |

                        ## 📌 **Notas**  
                        🔗 **Fuente:** 👉 [INE - Instituto Nacional de Estadística](https://www.ine.gob.bo)  
                        📅 **Frecuencia:** Datos anuales.  
                        📊 **Importancia:**  
                        - **Las reservas internacionales** incluyen **oro**, depósitos en bancos extranjeros y **activos líquidos** en moneda extranjera.  
                        - **Su variación** refleja la **capacidad del país para enfrentar crisis económicas**, intervenir en el mercado cambiario y cumplir con **obligaciones externas**.  
                        ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                ]
            ),
            dcc.Tab(
                label="Area Fiscal",
                style=tab_style,
                selected_style=tab_selected_style,
                children=[
                    dcc.Tabs(
                        children=[
                            dcc.Tab(
                                label="operaciones empresas publicas",
                                style=tab_style,
                                selected_style=tab_selected_style,
                                children=[
                                    dbc.Container(create_table_card("operaciones empresas publicas", df_operaciones_empresas_publicas), fluid=True),
                                    dbc.Container(estadisticas_operaciones_empresas_publicas, fluid=True),
                                    html.Div([
                                    html.Img(
                                        src='/assets/imagenes/16.operaciones_empresas_publicas/ingresos_totales.png',
                                        style={"width": "80%", "height": "auto", "marginBottom": "20px"}
                                    ),
                                    html.Img(
                                        src='/assets/imagenes/16.operaciones_empresas_publicas/egresos_totales.png',
                                        style={"width": "80%", "height": "auto", "marginBottom": "20px"}
                                    ),
                                    html.Img(
                                        src='/assets/imagenes/16.operaciones_empresas_publicas/resultado_fiscal_global.png',
                                        style={"width": "80%", "height": "auto", "marginBottom": "20px"}
                                    ),
                                    html.Img(
                                        src='/assets/imagenes/16.operaciones_empresas_publicas/operaciones_empresas_publicas_combined.png',
                                        style={"width": "80%", "height": "auto"}
                                    )
                                    ], className="d-flex justify-content-center", style={"flexDirection": "column", "alignItems": "center", "marginTop": "20px"}),
                                    dcc.Markdown('''
                                    # 📊 **Operaciones Consolidadas de Empresas Públicas (En % del PIB)**  

                                    ## 📌 **Descripción de la Tabla `operaciones_empresas_publicas`**  
                                    Esta tabla consolida las operaciones de las Empresas Públicas en Bolivia, expresadas en porcentaje del Producto Interno Bruto (PIB). Se registran los **ingresos totales**, **egresos totales** y el **resultado fiscal global** (superávit/ déficit).  

                                    ### 📄 **Columnas**  

                                    | **Columna**               | **Descripción**                                                            | **Unidad**         |
                                    |---------------------------|----------------------------------------------------------------------------|--------------------|
                                    | `año`                     | Año del registro                                                           | Año                |
                                    | `ingresos_totales`        | Ingresos totales de las Empresas Públicas                                  | % del PIB          |
                                    | `egresos_totales`         | Egresos totales de las Empresas Públicas                                   | % del PIB          |
                                    | `resultado_fiscal_global` | Resultado fiscal global (superávit / déficit) de las Empresas Públicas       | % del PIB          |

                                    ## 📌 **Notas**  
                                    - **(p) Preliminar:** Los datos de 2018, 2019 y 2020 se consideran preliminares.  
                                    - **1_/** Desde mayo de 2006, YPFB realiza operaciones de mayorista.  
                                    - **2_/** Desde 2005 no se registran ventas en el mercado externo y contratistas (por tratarse de operaciones de empresas capitalizadas). Desde 2007 se incluye la facturación de la venta de gas y petróleo de YPFB.  
                                    - **3_/** Desde mayo de 2007, por D.S. 29117, COMIBOL explota la reserva fiscal, que actualmente incluye las operaciones mineras de Huanuni.  
                                    - **4_/** Mediante D.S. 29026 en febrero de 2007, se nacionalizó la Empresa Metalúrgica Vinto, asumiendo nuevamente operaciones como entidad estatal tras su transferencia al sector privado en 1999.  

                                    **Fuente:** MEFP-VTCP – Dirección General de Administración y Finanzas Territoriales  
                                    **Elaboración:** MEFP-VTCP – Dirección General de Análisis y Políticas Fiscales  
                                    ''', style={"textAlign": "left", "fontSize": "16px", "lineHeight": "1.6"})
                                ]
                            )
                        ]
                    )
                ]
            ),
            # Tab para Asistente IA
            dcc.Tab(
                label="Asistente IA",
                style=tab_style,
                selected_style=tab_selected_style,
                children=[
                    dbc.Container([
                        html.H3("Asistente de Consultas Macroeconómicas", 
                                className="text-center my-4 text-secondary"),
                        dbc.Row([
                            dbc.Col(
                                dcc.Textarea(
                                    id="input_pregunta",
                                    placeholder=("Escribe tu consulta en lenguaje natural, por ejemplo:\n"
                                                 "- ¿Cuál fue el crecimiento del PIB en 2020?\n"
                                                 "- Muéstrame el gasto en consumo y formación de capital para el año 2015."),
                                    style={
                                        "width": "100%", 
                                        "height": "120px", 
                                        "borderRadius": "5px", 
                                        "padding": "10px",
                                        "fontFamily": "Arial, sans-serif",
                                        "fontSize": "14px"
                                    }
                                ), md=8
                            )
                        ], className="mb-3 justify-content-center"),
                        dbc.Row([
                            dbc.Col(
                                dbc.Button("Consultar", id="btn_consultar", color="primary", size="lg", n_clicks=0),
                                width="auto", className="text-center"
                            )
                        ], className="mb-3 justify-content-center"),
                        dbc.Row([
                            dbc.Col(
                                html.Div(id="output_respuesta", 
                                         style={
                                             "white-space": "pre-line",
                                             "border": "1px solid #ddd",
                                             "padding": "15px",
                                             "borderRadius": "5px",
                                             "backgroundColor": "#f8f9fa",
                                             "fontFamily": "Arial, sans-serif",
                                             "fontSize": "14px"
                                         }),
                                md=10
                            )
                        ], className="justify-content-center")
                    ], fluid=True)
                ]
            )
        ]
    )
# Viejo layout no utilizado
], fluid=True, style={"backgroundColor": "#e9ecef", "padding": "20px"})

# Nuevo layout simplificado
app.layout = create_main_layout()

# -----------------------------
# Callback: Procesar Consulta del Asistente IA
# -----------------------------
@app.callback(
    Output("output_respuesta", "children"),
    Input("btn_consultar", "n_clicks"),
    State("input_pregunta", "value")
)
def responder_consulta(n_clicks, pregunta):
    if n_clicks > 0 and pregunta:
        conn = sqlite3.connect("file:db/proyectomacro.db?mode=ro", uri=True)
        cursor = conn.cursor()
        # Generar consulta SQL usando LLM
        sql_query = generate_sql_from_question(pregunta)
        print("SQL generado:", sql_query)
        # Ejecutar la consulta en la base de datos
        try:
            if is_safe_query(sql_query):
                cursor.execute(sql_query)
                result = cursor.fetchall()
            else:
                result = "⚠️ Error: La consulta contiene operaciones no permitidas."
        except Exception as e:
            result = f"Error al ejecutar la consulta SQL: {e}"
        # Generar explicación con LLM
        explanation = generate_explanation(pregunta, sql_query, result)
        # Construir la respuesta final en formato Markdown
        response_text = (
            "**Consulta SQL generada:**\n"
            "```sql\n"
            f"{sql_query}\n"
            "```\n\n"
            "**Resultado:**\n"
            "```python\n"
            f"{result}\n"
            "```\n\n"
            "**Explicación:**\n"
            f"{explanation}"
        )
        return dcc.Markdown(response_text)

if __name__ == '__main__':
    app.run(debug=True)

