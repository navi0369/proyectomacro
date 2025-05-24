import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os
import numpy as np

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go

# Conectar a la base de datos y cargar los datos
conn = sqlite3.connect("../proyectomacro.db")
df = pd.read_sql("SELECT * FROM exportaciones_minerales_totales", conn)
df2 = pd.read_sql("SELECT * FROM precio_oficial_minerales", conn)
df.set_index('año', inplace=True)
df.index = df.index.astype(int)
conn.close()

df2.set_index('año', inplace=True)
df2.index = df2.index.astype(int)
df2 = df2.loc[1987:2023]

# Cerrar conexión (por si acaso)
conn.close()

# Factores de conversión
# Para minerales medidos en Libras Finas: zinc, estaño, plomo, cobre, wolfram
factor_lb = 1 / 0.453592   # ≈ 2.20462
# Para oro y plata medidos en Onzas Troy:
factor_ot = 1 / 0.0311035    # ≈ 32.1507
# Para antimonio medido en Toneladas Métricas Finas:
factor_tm = 1 / 1000         # Equivale a dividir entre 1000

# Conversión a USD por kilo fino para df2 (precios oficiales)
df2['zinc_kilo']      = df2['zinc'] * factor_lb
df2['estaño_kilo']    = df2['estaño'] * factor_lb
df2['plomo_kilo']     = df2['plomo'] * factor_lb
df2['cobre_kilo']     = df2['cobre'] * factor_lb
df2['wolfram_kilo']   = df2['wolfram'] * factor_lb
df2['oro_kilo']       = df2['oro'] * factor_ot
df2['plata_kilo']     = df2['plata'] * factor_ot
df2['antimonio_kilo'] = df2['antimonio'] * factor_tm
df2.head()

# Calcular el precio efectivo para cada mineral
# Fórmula: precio_efectivo = (valor * 1000) / volumen
minerales_lista = ["estaño", "plomo", "zinc", "plata", "wolfram", "cobre", "antimonio", "oro"]

for mineral in minerales_lista:
    vol_col = f"{mineral}_volumen"
    val_col = f"{mineral}_valor"
    precio_efectivo_col = f"{mineral}_precio_efectivo"
    df[precio_efectivo_col] = (df[val_col] * 1000) / df[vol_col]

# Definir carpeta de salida para las imágenes (si se requieren guardar imágenes estáticas)
output_dir = "../assets/imagenes/15.exportaciones_minerales"
os.makedirs(output_dir, exist_ok=True)

# --- Crear la aplicación Dash ---
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard de Exportaciones Minerales"),
    
    html.Div([
        html.Label("Selecciona un mineral:"),
        dcc.Dropdown(
            id="mineral-dropdown",
            options=[{"label": mineral.capitalize(), "value": mineral} for mineral in minerales_lista],
            value="zinc"
        )
    ], style={"width": "300px", "margin": "10px"}),

    html.Div(id="graphs-container"),
    html.Div(id="analysis-container", style={"margin-top": "20px", "fontSize": 16}),
    html.Div(id="graph-descriptions", style={"margin-top": "20px", "fontSize": 16})
])

@app.callback(
    [Output("graphs-container", "children"),
     Output("analysis-container", "children"),
     Output("graph-descriptions", "children")],
    [Input("mineral-dropdown", "value")]
)
def update_graphs(mineral):
    # Definir columnas de df
    vol_col = f"{mineral}_volumen"
    precio_efectivo_col = f"{mineral}_precio_efectivo"
    
    # Para el precio oficial en df2 usamos la columna correspondiente
    if mineral in ["oro", "plata", "antimonio", "estaño", "plomo", "zinc", "cobre", "wolfram"]:
        official_price_col = f"{mineral}_kilo"
    else:
        official_price_col = mineral

    # --- Gráfica Dual Axis: Volumen vs Precio Oficial ---
    trace_vol = go.Scatter(
        x=df.index,
        y=df[vol_col],
        mode="lines+markers",
        name="Volumen (kilos finos)",
        marker=dict(color='blue')
    )
    trace_price_official = go.Scatter(
        x=df2.index,
        y=df2[official_price_col],
        mode="lines+markers",
        name="Precio Oficial (USD)",
        marker=dict(color='red'),
        yaxis="y2"
    )
    layout_dual = go.Layout(
        title=f"{mineral.capitalize()}: Volumen vs Precio Oficial",
        xaxis=dict(title="Año"),
        yaxis=dict(title="Volumen (kilos finos)", titlefont=dict(color="blue")),
        yaxis2=dict(
            title="Precio Oficial (USD)",
            titlefont=dict(color="red"),
            overlaying="y",
            side="right"
        ),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    dual_axis_fig = go.Figure(data=[trace_vol, trace_price_official], layout=layout_dual)

    # --- Gráfica de Precio Efectivo ---
    trace_pe = go.Scatter(
        x=df.index,
        y=df[precio_efectivo_col],
        mode="lines+markers",
        name="Precio Efectivo",
        marker=dict(color='green')
    )
    layout_pe = go.Layout(
        title=f"{mineral.capitalize()}: Precio Efectivo",
        xaxis=dict(title="Año"),
        yaxis=dict(title="Precio Efectivo (USD por unidad)"),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    pe_fig = go.Figure(data=[trace_pe], layout=layout_pe)

    # Contenedor de gráficas
    graphs = html.Div([
        dcc.Graph(figure=dual_axis_fig),
        dcc.Graph(figure=pe_fig)
    ])

    # --- Análisis Numérico Simple ---
    # Se utiliza el primer y último año del DataFrame para calcular la variación acumulada
    min_year = df.index.min()
    max_year = df.index.max()
    
    # Ingresos = valor exportado en USD (valor * 1000)
    revenue_first = df.loc[min_year, f"{mineral}_valor"] * 1000
    revenue_last  = df.loc[max_year, f"{mineral}_valor"] * 1000
    delta_log_revenue = np.log(revenue_last) - np.log(revenue_first)
    
    # Precio efectivo
    price_first = df.loc[min_year, f"{mineral}_precio_efectivo"]
    price_last  = df.loc[max_year, f"{mineral}_precio_efectivo"]
    delta_log_price = np.log(price_last) - np.log(price_first)
    
    # Volumen exportado
    volume_first = df.loc[min_year, vol_col]
    volume_last  = df.loc[max_year, vol_col]
    delta_log_volume = np.log(volume_last) - np.log(volume_first)
    
    # Para evitar división por cero, verificamos que delta_log_revenue sea distinto de cero
    if delta_log_revenue != 0:
        price_contrib = (delta_log_price / delta_log_revenue) * 100
        volume_contrib = (delta_log_volume / delta_log_revenue) * 100
    else:
        price_contrib, volume_contrib = 0, 0

    analysis = html.Div([
        html.H3("Análisis Numérico del Crecimiento de Ingresos"),
        html.P(f"Período analizado: {min_year} a {max_year}."),
        html.P(f"Para {mineral.capitalize()}:"),
        html.Ul([
            html.Li(f"Contribución del precio: {price_contrib:.2f}%"),
            html.Li(f"Contribución del volumen: {volume_contrib:.2f}%")
        ]),
        html.P("Si la contribución del precio es mayor, el aumento de ingresos se debe principalmente a mejores precios. "
               "Si la contribución del volumen es mayor, se debe a un incremento en la cantidad exportada.")
    ])

    # --- Descripción de las Gráficas ---
    description_text = html.Div([
        html.H3("Descripción de las Gráficas"),
        html.P("La primera gráfica (dual axis) muestra en un mismo gráfico el volumen exportado (línea azul) y el precio oficial (línea roja) para el mineral seleccionado. "
               "Permite analizar la relación entre la cantidad exportada y la cotización del mercado."),
        html.P("La segunda gráfica presenta el precio efectivo, calculado como el valor exportado (convertido de miles de USD a USD) dividido por el volumen exportado (en kilos finos). "
               "Este indicador refleja el ingreso promedio obtenido por cada unidad exportada y ayuda a determinar si los ingresos aumentan por mejores precios o por mayor volumen.")
    ])

    return graphs, analysis, description_text

if __name__ == "__main__":
    app.run_server( debug=True)