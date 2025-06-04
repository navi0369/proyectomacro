Proyecto Macro – Estructura de Base de Datos

Base SQLite: proyectomacro.db

Última actualización: 21 de mayo de 2025Fuente original de los detalles: Informe «TABLAS_BASE_DE_DATOS.pdf»

Cómo usar este documento con ChatGPT Codex

Copia al prompt sólo las secciones que necesites – no envíes todo el archivo si tu consulta es puntual.

Incluye nombre de la tabla, periodo y campos cuando pidas consultas SQL, para que Codex entienda exactamente la estructura.

Si añades tablas nuevas o cambias columnas, actualiza este README y vuelve a entrenar el contexto de Codex.

Índice

Cuentas Nacionales / PIB

Sector Externo / Balanza Comercial

Exportaciones

Importaciones

Precios y Producción

Sector Fiscal

Deuda

1. Cuentas Nacionales / PIB

1.1 PIB_Real_Gasto

Campo

Tipo

Descripción

año

INTEGER

Año del registro

gastos_consumo

REAL

Consumo total (miles de Bs 1990)

formacion_capital

REAL

Formación bruta de capital

exportacion_bienes_servicios

REAL

Exportaciones de bienes y servicios

importacion_bienes

REAL

Importaciones de bienes

pib_real_base_1990

REAL

PIB real (base 1990)

consumo_privado

REAL

Consumo privado

consumo_publico

REAL

Consumo público

Periodo: 1950 – 2023 · Unidad: Miles de bolivianos 1990_

1.2 pib_ramas

Campo

Tipo

Descripción

año

INTEGER

Año

agropecuario

REAL

Agricultura, silvicultura, pesca

minas_canteras_total

REAL

Minería + petróleo

mineria

REAL

Minería (sub‑rubro)

petroleo

REAL

Petróleo (sub‑rubro)

industria_manufacturera

REAL

Industria manufacturera

construcciones

REAL

Construcciones

energia

REAL

Electricidad, gas, agua

transportes

REAL

Transportes y comunicaciones

comercio_finanzas

REAL

Comercio y finanzas

gobierno_general

REAL

Gobierno general

propiedad_vivienda

REAL

Propiedad de vivienda

servicios

REAL

Servicios varios

derechos_imp

REAL

Derechos de importación / impuestos

pib_nominal

REAL

PIB nominal

pib_real

REAL

PIB real

Periodo: 1950 – 2022 · Unidad: Miles de Bs 1990_

1.3 Participacion_PIB

Campo

Tipo

Descripción

año

INTEGER

Año

exportaciones_pib

REAL

Exportaciones / PIB (%)

importaciones_pib

REAL

Importaciones / PIB (%)

Periodo: 1950 – 2023 · Unidad: Porcentaje_

1.4 tasa_crecimiento_pib

Campo

Tipo

Descripción

año

INTEGER

Año

crecimiento

REAL

Tasa de crecimiento anual (%)

Periodo: 1951 – 2024 · Unidad: Porcentaje_

1.5 participacion_x_m_pib

Campo

Tipo

Descripción

año

INTEGER

Año

x

REAL

Exportaciones / PIB (%)

m

REAL

Importaciones / PIB (%)

Periodo: 1950 – 2023_

1.6 participacion_pib_ramas

Campo

Tipo

Descripción

año

INTEGER

Año

agropecuario

REAL

% PIB

minas_canteras_total

REAL

% PIB

mineria

REAL

% PIB

petroleo

REAL

% PIB

industria_manufacturera

REAL

% PIB

construcciones

REAL

% PIB

energia

REAL

% PIB

transportes

REAL

% PIB

comercio_finanzas

REAL

% PIB

gobierno_general

REAL

% PIB

propiedad_vivienda

REAL

% PIB

servicios

REAL

% PIB

Periodo: 1950 – 2023 · Unidad: Porcentaje_

2. Sector Externo / Balanza Comercial

2.1 balanza_comercial

Campo

Tipo

Descripción

año

INTEGER

Año

exportaciones

REAL

Exportaciones (M USD)

importaciones

REAL

Importaciones (M USD)

saldo_comercial

REAL

Exportaciones − Importaciones (M USD)

Periodo: 1949 – 2024 · Unidad: Millones USD_

2.2 flujo_divisas

Campo

Tipo

Descripción

año

INTEGER

Año

ingreso_divisas

REAL

Ingresos de divisas (M USD)

egreso_divisas

REAL

Egresos de divisas (M USD)

flujo_neto_divisas

REAL

Ingresos − Egresos (M USD)

Periodo: 1985 – 2023 · Unidad: Millones USD_

2.3 grado_de_apertura

Campo

Tipo

Descripción

año

INTEGER

Año

grado

REAL

((X + M) / PIB) %

Periodo: 1950 – 2022 · Unidad: Porcentaje_

2.4 Reservas_oro_divisas

Campo

Tipo

Descripción

año

INTEGER

Año

reservas_totales

REAL

Reservas internacionales (M USD)

Periodo: 1950 – 2023 · Unidad: Millones USD_

3. Exportaciones

(sección abreviada aquí; ver archivo completo para todas las tablas)

Tabla

Periodo

Descripción breve

exportaciones_totales

1980‑2023

Valor tradicional / no tradicional

exportaciones_minerales_totales

1952‑2023

Volumen y valor de 8 minerales

exportaciones_tradicionales

1992‑2024

Minerales vs. hidrocarburos

exportaciones_tradicionales_no_tradicionales

1980‑2024

Desglose total

participacion_exp_trad_no_trad

1980‑2023

% tradicionales vs no trad

exportaciones_tradicionales_hidrocarburos

1992‑2024

Gas natural y otros

exportacion_gas_natural

1987‑2023

Volumen, precio, valor

…

…

ver detalle completo en PDF

(Para cada tabla de esta sección encontrarás esquema completo en las páginas 14‑24 del PDF fuente)

4. Importaciones

Tabla

Periodo

Descripción breve

composicion_importaciones_uso_destino

1980‑2024

Valor CIF por categoría

participacion_composicion_importaciones_uso_destino

1980‑2024

% por categoría

tu

1992‑2024

Exportaciones no tradicionales detalladas

5. Precios y Producción

Tabla

Periodo

Descripción breve

precio_minerales

1980‑2015

Precio real de minerales

precio_oficial_minerales

1950‑2024

Precios oficiales

precio_petroleo_wti

1996‑2023

Precio WTI (USD/barril)

produccion_minerales

1985‑2021

Producción de 8 minerales

6. Sector Fiscal

Tabla

Periodo

Descripción breve

consolidado_spnf

1990‑2023

Ingresos, egresos, saldo

operaciones_empresas_publicas

1990‑2020

% PIB de EEPPs

inversion_publica_total

1990‑2023

Inversión total (k USD)

inversion_publica_por_sectores

1990‑2014

Inversión por sector

7. Deuda

Tabla

Periodo

Descripción breve

deuda_externa_total

1951‑2020

Stock de deuda externa (M USD)

deuda_interna

1993‑2022

Stock de deuda interna (M USD)

Notas finales

Las columnas año funcionan como clave primaria en casi todas las tablas.

Salvo que se indique lo contrario, los valores monetarios están expresados en millones USD o miles de bolivianos 1990.

Para series con datos preliminares, se etiquetaron los últimos años como (p).

Este README se deriva directamente del PDF original; si agregas columnas o corriges periodos, edita aquí también.

Fin del archivo

