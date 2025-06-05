
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
"""Dashboard interactivo para analizar la relación entre precios internacionales,
exportaciones y estabilidad económica en Bolivia."""

import pandas as pd
import sqlite3
import os
import statsmodels.api as sm
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px

# %%
# Conexión y carga de datos
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "db", "proyectomacro.db")
conn = sqlite3.connect(DB_PATH)
crecimiento = pd.read_sql("SELECT año, crecimiento FROM Tasa_Crecimiento_PIB", conn)
exportaciones = pd.read_sql("SELECT año, total_valor_oficial FROM exportaciones_totales", conn)
precios_minerales = pd.read_sql(
    "SELECT año, zinc, estaño, plata, oro, cobre FROM precio_oficial_minerales",
    conn
)
precio_petroleo = pd.read_sql("SELECT año, precio FROM precio_petroleo_wti", conn)
conn.close()

for df in [crecimiento, exportaciones, precios_minerales, precio_petroleo]:
    df['año'] = df['año'].astype(int)

precios_minerales['precio_minerales_promedio'] = precios_minerales[
    ['zinc', 'estaño', 'plata', 'oro', 'cobre']
].mean(axis=1)

merged = (
    crecimiento.merge(exportaciones, on='año', how='left')
    .merge(precio_petroleo, on='año', how='left')
    .merge(precios_minerales[['año', 'precio_minerales_promedio']], on='año', how='left')
)

# %%
# Cálculo de correlaciones y modelo
corr_cols = ['crecimiento', 'total_valor_oficial', 'precio', 'precio_minerales_promedio']
correlation = merged[corr_cols].corr()
reg_data = merged.dropna(subset=corr_cols)
X = sm.add_constant(reg_data[['total_valor_oficial', 'precio', 'precio_minerales_promedio']])
y = reg_data['crecimiento']
model = sm.OLS(y, X).fit()

# %%
# Crear figuras con Plotly
fig_line_exports = px.line(
    merged, x='año', y=['crecimiento', 'total_valor_oficial'],
    labels={'value':'Valor', 'variable':'Serie'}, title='Crecimiento del PIB y Exportaciones Totales'
)

fig_line_prices = px.line(
    merged, x='año', y=['crecimiento', 'precio_minerales_promedio', 'precio'],
    labels={'value':'Valor', 'variable':'Serie'}, title='Crecimiento del PIB y Precios Internacionales'
)

fig_scatter_exports = px.scatter(
    reg_data, x='total_valor_oficial', y='crecimiento', trendline='ols',
    labels={'total_valor_oficial':'Exportaciones Totales (MM USD)', 'crecimiento':'Crecimiento PIB (%)'},
    title='Crecimiento del PIB vs Exportaciones Totales'
)

fig_scatter_prices = px.scatter(
    reg_data, x='precio_minerales_promedio', y='crecimiento', trendline='ols',
    labels={'precio_minerales_promedio':'Precio minerales promedio (USD)', 'crecimiento':'Crecimiento PIB (%)'},
    title='Crecimiento del PIB vs Precio de Minerales'
)

# %%
# Construcción de la app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

def correlation_table(df):
    return dash_table.DataTable(
        data=df.round(3).reset_index().to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.reset_index().columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center', 'padding': '5px'},
    )

app.layout = dbc.Container([
    html.H2('Relación Precios Internacionales, Exportaciones y Crecimiento del PIB', className='my-3 text-center'),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_line_exports), md=6),
        dbc.Col(dcc.Graph(figure=fig_line_prices), md=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_scatter_exports), md=6),
        dbc.Col(dcc.Graph(figure=fig_scatter_prices), md=6),
    ]),
    html.H4('Matriz de Correlación', className='mt-4'),
    correlation_table(correlation),
    html.H4('Resumen del Modelo de Regresión', className='mt-4'),
    html.Pre(model.summary().as_text(), style={'whiteSpace': 'pre-wrap', 'fontFamily':'monospace'})
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)