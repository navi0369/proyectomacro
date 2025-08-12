# Cuentas Nacionales / PIB

## 1. Listado

- **Nombre de tabla:** `PIB_Real_Gasto`
- **Nombre descriptivo:** PIB real (base 1990) desagregado por componentes de gasto

## 2. Estructura

- **Descripción:** Datos anuales de consumo, inversión, exportaciones, importaciones y PIB real de Bolivia.
- **Periodo:** 1950--2023
- **Unidad base:** Miles de bolivianos constantes de 1990
- **Fuente original:** Archivo Excel `reports/pruebas.xls`
- **Notas:** Ninguna

## 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `gastos_consumo` | REAL | Consumo total (miles de Bs. 1990) |
| `formacion_capital` | REAL | Inversión (formación bruta de capital) |
| `exportacion_bienes_servicios` | REAL | Exportaciones de bienes y servicios |
| `importacion_bienes` | REAL | Importaciones de bienes |
| `pib_real_base_1990` | REAL | PIB real (base 1990) |
| `consumo_privado` | REAL | Consumo privado |
| `consumo_publico` | REAL | Consumo público |

## 4. Procesamiento aplicado

Ninguno.
## Desagregación del PIB por ramas de actividad

### 1. Listado

- **Nombre de tabla:** `pib_ramas`
- **Nombre descriptivo:** Desagregación del PIB por sectores económicos

### 2. Estructura

- **Descripción:** Valores anuales del PIB clasificados por ramas de actividad, para analizar la contribución sectorial.
- **Periodo:** 1950--2022
- **Unidad base:** Miles de bolivianos constantes de 1990
- **Fuente original:** Archivo Excel `db/pruebas.xlsx`
- **Notas:** Datos preliminares para 2019–2022

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `agropecuario` | REAL | Actividad agropecuaria |
| `minas_canteras_total` | REAL | Minería y petróleo (rubro 2 total) |
| `mineria` | REAL | Minería (rubro 2.1) |
| `petroleo` | REAL | Petróleo (rubro 2.2) |
| `industria_manufacturera` | REAL | Industria manufacturera (rubro 3) |
| `construcciones` | REAL | Construcciones (rubro 4) |
| `energia` | REAL | Producción energética (rubro 5) |
| `transportes` | REAL | Transportes (rubro 6) |
| `comercio_finanzas` | REAL | Comercio y finanzas (rubros 7–8) |
| `gobierno_general` | REAL | Gobierno general (rubro 9) |
| `propiedad_vivienda` | REAL | Propiedad de vivienda (rubro 10) |
| `servicios` | REAL | Servicios (rubro 11) |
| `derechos_imp` | REAL | Derechos de importación / impuestos |
| `pib_nominal` | REAL | Producto Interno Bruto nominal |
| `pib_real` | REAL | Producto Interno Bruto real |

### 4. Procesamiento aplicado

Ninguno.
## Participación de Exportaciones e Importaciones en el PIB

### 1. Listado

- **Nombre de tabla:** `Participacion_PIB`
- **Nombre descriptivo:** Participación de exportaciones e importaciones en el PIB

### 2. Estructura

- **Descripción:** Exportaciones e importaciones expresadas como porcentaje del PIB; mide el peso relativo de X y M en la actividad económica.
- **Periodo:** 1950--2023
- **Unidad base:** Porcentaje
- **Fuente original:** Archivo Excel `reports/pruebas.xls`
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `exportaciones_pib` | REAL | Exportaciones como % del PIB |
| `importaciones_pib` | REAL | Importaciones como % del PIB |

### 4. Procesamiento aplicado

Ninguno.
## Tasa de Crecimiento Anual del PIB

### 1. Listado

- **Nombre de tabla:** `tasa_crecimiento_pib`
- **Nombre descriptivo:** Tasa de crecimiento anual del Producto Interno Bruto

### 2. Estructura

- **Descripción:** Variación porcentual anual del PIB para evaluar el ritmo de crecimiento económico.
- **Periodo:** 1951--2024
- **Unidad base:** Porcentaje
- **Fuente original:** Archivo Excel `db/pruebas.xlsx`
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `crecimiento` | REAL | Tasa de crecimiento anual del PIB (%) |

### 4. Procesamiento aplicado

Ninguno.
## Participación de Exportaciones e Importaciones en el PIB (`participacion_x_m_pib`)

### 1. Listado

- **Nombre de tabla:** `participacion_x_m_pib`
- **Nombre descriptivo:** Participación de X (exportaciones) y M (importaciones) en el PIB

### 2. Estructura

- **Descripción:** Porcentaje que representan las exportaciones (X) y las importaciones (M) sobre el PIB anual, para medir su incidencia en la actividad económica.
- **Periodo:** 1950--2023
- **Unidad base:** Porcentaje
- **Fuente original:** Archivo Excel `db/pruebas.xlsx`
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `x` | REAL | Exportaciones como % del PIB |
| `m` | REAL | Importaciones como % del PIB |

### 4. Procesamiento aplicado

Ninguno.
### 1. Listado

- **Nombre de tabla:** `exportaciones_tradicionales_hidrocarburos`
- **Nombre descriptivo:** Exportaciones de hidrocarburos, gas natural y otros hidrocarburos

### 2. Estructura

- **Descripción:** Valores anuales de exportaciones de hidrocarburos, desglosados en gas natural y otros hidrocarburos, para evaluar su contribución al comercio exterior.
- **Periodo:** 1992--2024
- **Unidad base:** Millones de dólares
- **Fuente original:** INE — https://www.ine.gob.bo/index.php/estadisticas-economicas/comercio-exterior/cuadros-estadisticos-exportaciones/
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `hidrocarburos` | REAL | Total hidrocarburos (millones USD) |
| `gas_natural` | REAL | Gas natural (millones USD) |
| `otros_hidrocarburos` | REAL | Otros hidrocarburos (millones USD) |

### 4. Procesamiento aplicado

Ninguno.
## Participación del PIB por ramas de actividad

(`participacion_pib_ramas`)}
### 1. Listado

- **Nombre de tabla:** `participacion_pib_ramas`
- **Nombre descriptivo:** Porcentaje del PIB desagregado por ramas de actividad económica

### 2. Estructura

- **Descripción:** Porcentaje anual que representa cada rama de actividad sobre el Producto Interno Bruto.
- **Periodo:** 1950--2023
- **Unidad base:** Porcentaje (%)
- **Fuente original:** Base de datos SQLite (`participacion.db`) construido a partir de archivos Excel.
- **Notas:**
  - `minas_canteras_total` calculado como suma de `mineria` + `petroleo`.
  - `comercio_finanzas` corresponde a la suma de:
  - `comercio` (rubro 6)
  - `servicios_financieros` (parte del rubro 8)
  - `servicios_a_empresas` (parte del rubro 8)
  -  texttt restaurantes_y_hoteles (rubro 10)
  - Valores provisionales marcados “(p)” para 2018–2023.

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro (PK) |
| `agropecuario` | REAL | Agricultura, silvicultura, caza y pesca (% PIB) |
| `minas_canteras_total` | REAL | Minería + petróleo (% PIB) |
| `mineria` | REAL | Minerales metálicos y no metálicos (% PIB) |
| `petroleo_crudo_y_gas_natural` | REAL | Petróleo crudo y gas natural (% PIB) |
| `industria_manufacturera` | REAL | Industria manufacturera (% PIB) |
| `construcciones` | REAL | Construcción (% PIB) |
| `energia` | REAL | Electricidad, gas y agua (% PIB) |
| `transportes` | REAL | Transporte, almacenamiento y comunicaciones |
| `comercio_finanzas` | REAL | Comercio y servicios financieros/empresas |
| `gobierno_general` | REAL | Gobierno general |
| `propiedad_vivienda` | REAL | Propiedad de vivienda) |
| `servicios` | REAL | Servicios comunales, sociales, personales y hoteles |

### 4. Procesamiento aplicado

- Cálculo de agregados:
  - `minas_canteras_total` = `mineria` + `petroleo`.
  - `comercio_finanzas` = `comercio` + `servicios_financieros` + `servicios_a_empresas`, excluyendo `propiedad_vivienda`.
- Inserción manual de valores porcentuales año a año a partir de fuentes Excel y estimados provisionales.

## PIB a precios corrientes por tipo de gasto

### 1. Listado

- **Nombre de tabla:** `pib_nominal_gasto`
- **Nombre descriptivo:** PIB a precios corrientes por tipo de gasto

### 2. Estructura

- **Descripción:** Valores anuales del PIB a precios corrientes desagregado por enfoque del gasto.
- **Periodo:** 1980–2023
- **Unidad base:** Miles de bolivianos
- **Fuente original:** INE: https://nube.ine.gob.bo/index.php/s/Sx5vznBqGGGIuN2/download
- **Notas:** 2017 al 2023 datos preliminares

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año del registro |
| gastos_consumo | REAL | Consumo total (miles de bolivianos) |
| consumo_privado | REAL | Gasto de consumo final de los hogares e ISFLSH |
| consumo_publico | REAL | Gasto de consumo final de la administración pública |
| variacion_existencias | REAL | Variación de existencias |
| formacion_capital | REAL | Formación bruta de capital fijo |
| exportacion_bienes_servicios | REAL | Exportaciones de bienes y servicios |
| importacion_bienes | REAL | Importaciones de bienes y servicios |
| pib_a_precios_corrientes | REAL | PIB a precios de mercado |

### 4. Procesamiento aplicado

Se agregó `gastos_consumo`, que es la suma de `consumo_privado` y `consumo_publico`.
## Deflactor implícito del PIB por tipo de gasto

### 1. Listado

- **Nombre de tabla:** `deflactor_implicito_pib_gasto`
- **Nombre descriptivo:** Índices de precios implícitos del PIB por tipo de gasto

### 2. Estructura

- **Descripción:** Deflactor implícito del PIB desagregado por componentes de gasto (base 1990).
- **Periodo:** 1980–2023
- **Unidad base:** Índice (1990 = 100)
- **Fuente original:** UDAPE: https://dossier.udape.gob.bo/res/DEFLACTOR%20IMPL%C3%8DCITO%20DEL%20PIB%20POR%20TIPO%20DE%20GASTO
- **Notas:** Datos preliminares 2017–2023; base en 1990.

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año de referencia |
| consumo_publico | REAL | Deflactor de consumo público |
| consumo_hogares | REAL | Deflactor de consumo de los hogares e ISFLSH |
| variacion_existencias | REAL | Deflactor de variación de existencias |
| formacion_capital_fijo | REAL | Deflactor de formación bruta de capital fijo |
| exportaciones | REAL | Deflactor de exportaciones de bienes y servicios |
| importaciones | REAL | Deflactor de importaciones de bienes y servicios |
| pib_precios_mercado | REAL | Deflactor implícito del PIB a precios de mercado (índice) |

### 4. Procesamiento aplicado

Ninguno.
## Oferta total y componentes

### 1. Listado

- **Nombre de tabla:** `oferta_total`
- **Nombre descriptivo:** Oferta total y sus componentes (a precios de mercado)

### 2. Estructura

- **Descripción:** Serie anual de la oferta total de la economía boliviana, desglosada en producción bruta (VBP), importaciones y ajustes impositivos/logísticos.
- **Periodo:** 1988–2023
- **Unidad base:** Miles de bolivianos constantes de 1990
- **Fuente original:** INE – Oferta total y demanda total https://www.ine.gob.bo/index.php/estadisticas-economicas/pib-y-cuentas-nacionales/producto-interno-bruto-anual/oferta-total-y-demanda-total/
- **Notas:** cifras preliminares etiquetadas “(p)” a partir de 2017

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año del registro |
| oferta_total | REAL | Oferta total a precios de mercado |
| produccion_bruta | REAL | Valor Bruto de la Producción (VBP) |
| importaciones | REAL | Importaciones de bienes y servicios |
| derechos_imp | REAL | Derechos sobre importaciones |
| impuestos_ind | REAL | IVA, IT y otros impuestos indirectos |
| margenes_transp | REAL | Márgenes de comercialización y transporte |

### 4. Procesamiento aplicado

- Conversión manual de cifras con separador de miles “,” a números puros.
- Tipado `REAL` para permitir promedios y tasas de crecimiento.
- Valores preliminares (2017–2023) marcados con sufijo “p”.

## Demanda total y componentes

### 1. Listado

- **Nombre de tabla:** `demanda_total`
- **Nombre descriptivo:** Demanda total y sus componentes (a precios de mercado)

### 2. Estructura

- **Descripción:** Serie anual de la demanda total de la economía boliviana, desglosada en consumo intermedio, consumo final, formación bruta de capital fijo, variación de existencias y exportaciones de bienes y servicios.
- **Periodo:** 1988–2023
- **Unidad base:** Miles de bolivianos constantes de 1990
- **Fuente original:** INE – Oferta total y demanda total https://www.ine.gob.bo/index.php/estadisticas-economicas/pib-y-cuentas-nacionales/producto-interno-bruto-anual/oferta-total-y-demanda-total/
- **Notas:** cifras preliminares etiquetadas “(p)” a partir de 2017

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| anio | INTEGER PRIMARY KEY | Año del registro |
| demanda_total | REAL | Demanda total a precios de mercado |
| consumo_intermedio | REAL | Consumo intermedio |
| consumo_final | REAL | Consumo final |
| fbcf | REAL | Formación Bruta de Capital Fijo |
| variacion_existencias | REAL | Variación de existencias |
| exportaciones_bienes_serv | REAL | Exportaciones de bienes y servicios |

### 4. Procesamiento aplicado

- Eliminación manual de separadores de miles (“,”) en cifras.
- Tipado `REAL` para facilitar cálculos de tasas y promedios.
- Valores preliminares marcados con sufijo “(p)”.

## VBP por ramas de actividad económica (`vbp_sector_2006_2014`)

### 1. Listado

- **Nombre de tabla:** `vbp_sector_2006_2014`
- **Nombre descriptivo:** Valor Bruto de Producción por rama de actividad económica, 2006--2014

### 2. Estructura

- **Descripción:** Serie anual del Valor Bruto de Producción (VBP) desagregado en 35 ramas de actividad económica, expresado en miles de bolivianos de 1990.
- **Periodo:** 2006--2014
- **Unidad base:** Miles de bolivianos constantes de 1990
- **Fuente original:** INE – Matrices de insumo-producto https://www.ine.gob.bo/index.php/estadisticas-economicas/pib-y-cuentas-nacionales/matrices/matrices-de-insumo-producto/
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER PRIMARY KEY | Año |
| `productos_agricolas_no_industriales` | REAL | VBP |
| `productos_agricolas_industriales` | REAL | VBP |
| `coca` | REAL | VBP |
| `productos_pecuarios` | REAL | VBP |
| `silvicultura_caza_y_pesca` | REAL | VBP |
| `petroleo_crudo_y_gas_natural` | REAL | VBP |
| `minerales_metalicos_y_no_metalicos` | REAL | VBP |
| `carnes_frescas_y_elaboradas` | REAL | VBP |
| `productos_lacteos` | REAL | VBP |
| `productos_de_molineria_y_panaderia` | REAL | VBP |
| `azucar_y_confiteria` | REAL | VBP |
| `productos_alimenticios_diversos` | REAL | VBP |
| `bebidas` | REAL | VBP |
| `tabaco_elaborado` | REAL | VBP |
| `textiles_prendas_vestir_y_productos_del_cuero` | REAL | VBP |
| `madera_y_productos_de_madera` | REAL | VBP |
| `papel_y_productos_de_papel` | REAL | VBP |
| `substancias_y_productos_quimicos` | REAL | VBP |
| `productos_de_refinacion_del_petroleo` | REAL | VBP |
| `productos_de_minerales_no_metalicos` | REAL | VBP |
| `productos_basicos_de_metales` | REAL | VBP |
| `productos_metalicos_maquinaria_y_equipo` | REAL | VBP |
| `productos_manufacturados_diversos` | REAL | VBP |
| `electricidad_gas_y_agua` | REAL | VBP |
| `construccion` | REAL | VBP |
| `comercio` | REAL | VBP |
| `transporte_y_almacenamiento` | REAL | VBP |
| `comunicaciones` | REAL | VBP |
| `servicios_financieros` | REAL | VBP |
| `servicios_a_las_empresas` | REAL | VBP |
| `propiedad_de_vivienda` | REAL | VBP |
| `servicios_comunales_sociales_y_personales` | REAL | VBP |
| `restaurantes_y_hoteles` | REAL | VBP |
| `servicios_domesticos` | REAL | VBP |
| `servicios_de_la_administracion_publica` | REAL | VBP |

### 4. Procesamiento aplicado

Ninguno.
## Balanza de Pagos (`balanza_de_pagos`)

### 1. Listado

- **Nombre de tabla:** `balanza_de_pagos`
- **Nombre descriptivo:** Balanza de pagos — resumen de cuentas principales

### 2. Estructura

- **Descripción:** Registro anual de las cinco partidas contables principales de la balanza de pagos boliviana: cuenta corriente, cuenta capital, errores y omisiones, saldo global y financiamiento.
- **Periodo:** 1980--2023
- **Unidad base:** Millones de dólares estadounidenses (USD)
- **Fuente original:** https://dossier.udape.gob.bo/res/balanza%20de%20pagos
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `current_account` | REAL | I. Cuenta corriente (1+2+3+4) |
| `capital_account` | REAL | II. Cuenta capital (1+2+3+4+5+6+7) |
| `errors_omissions` | REAL | III. Errores y omisiones |
| `bop_balance` | REAL | IV. Superávit o déficit de BdeP (I + II + III) |
| `financing` | REAL | V. Financiamiento (1+2+3) |

### 4. Procesamiento aplicado

Ninguno.
## PIB per cápita (US$ corrientes) — Bolivia

### 1. Listado

- **Nombre de tabla:** `pib_percapita`
- **Nombre descriptivo:** PIB per cápita (US$ a precios actuales)

### 2. Estructura

- **Descripción:** Serie anual del PIB per cápita de Bolivia en dólares corrientes (indicador del Banco Mundial NY.GDP.PCAP.CD).
- **Periodo:** 1960--2024
- **Unidad base:** US$ corrientes por habitante
- **Fuente original:** Banco Mundial, indicador `NY.GDP.PCAP.CD`. https://datos.bancomundial.org/indicator/NY.GDP.PCAP.CD?locations=BOL
- **Notas:** Valores tal como los provee el Banco Mundial (sin ajustes locales). Posibles revisiones históricas; el dato de 2024 puede ser preliminar.

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `pib_percapita` | REAL | PIB per cápita (US$ corrientes) |

### 4. Procesamiento aplicado

- Filtrado de la fila con `Country Code = BOL`.
- Selección de columnas anuales 1960--2024 y pivoteo a formato `(año, pib_percapita)`.
- Conversión de tipos: `año` textrightarrow{} INTEGER, `pib_percapita` textrightarrow{} REAL.
- Sin imputación ni suavizado; se preservan los valores originales del Banco Mundial.

# Sector Externo / Balanza Comercial

## 1. Listado

- **Nombre de tabla:** `balanza_comercial`
- **Nombre descriptivo:** Balanza comercial en millones de USD

## 2. Estructura

- **Descripción:** Registro anual del valor de exportaciones, importaciones y saldo comercial de Bolivia.
- **Periodo:** 1949--2024
- **Unidad base:** Millones de dólares
- **Fuente original:**
  - https://nube.ine.gob.bo/index.php/s/nMPCP2wBQqnx7c1/download
  - Memorias del Banco Central de Bolivia
- **Notas:** Los valores no fueron modificados.

## 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `exportaciones` | REAL | Valor de exportaciones (millones USD) |
| `importaciones` | REAL | Valor de importaciones (millones USD) |
| `saldo_comercial` | REAL | Exportaciones -- Importaciones (millones USD) |

## 4. Procesamiento aplicado

Ninguno.
## Flujo de Divisas del Sector Externo (`flujo_divisas`)

### 1. Listado

- **Nombre de tabla:** `flujo_divisas`
- **Nombre descriptivo:** Flujo de divisas: ingresos, egresos y flujo neto

### 2. Estructura

- **Descripción:** Registra anualmente los ingresos y egresos de divisas en Bolivia, así como el flujo neto, para evaluar la balanza de transacciones internacionales.
- **Periodo:** 1985--2023
- **Unidad base:** Millones de dólares
- **Fuente original:** https://dossier.udape.gob.bo/res/balanza%20cambiaria
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `ingreso_divisas` | REAL | Ingresos de divisas (millones USD) |
| `egreso_divisas` | REAL | Egresos de divisas (millones USD) |
| `flujo_neto_divisas` | REAL | Flujo neto (Ingresos – Egresos) |

### 4. Procesamiento aplicado

Ninguno.
## Grado de Apertura Económica (`grado_de_apertura`)

### 1. Listado

- **Nombre de tabla:** `grado_de_apertura`
- **Nombre descriptivo:** Grado de apertura económica de Bolivia

### 2. Estructura

- **Descripción:** Indicador que mide la apertura económica como la suma de exportaciones e importaciones en relación al PIB anual.
- **Periodo:** 1950--2022
- **Unidad base:** Porcentaje
- **Fuente original:**
  - Archivo Excel `db/pruebas.xlsx` 1960--2022  Fuente que se utilizó para calcular los datos de 2023 y 2024
  - Banco Mundial, https://datos.bancomundial.org/indicador/NY.GDP.MKTP.CD?end=2024&locations=BO&start=2016
  - tabla: grado_de_apertura
- **Notas:** desde para calcular los valores de 2023 se usaron los datos de la tabla balanza_comercial (para obtener X y M) y los datos que el banco mundial proporciona sobre pib en dolares

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `grado` | REAL | Grado de apertura económica (% del PIB) |

### 4. Procesamiento aplicado

Ninguno.
## Reservas Internacionales de Oro y Divisas (`Reservas_oro_divisas`)

### 1. Listado

- **Nombre de tabla:** `Reservas_oro_divisas`
- **Nombre descriptivo:** Reservas internacionales de oro y otras divisas

### 2. Estructura

- **Descripción:** Volumen anual de reservas internacionales en oro y divisas, expresado en millones de dólares.
- **Periodo:** 1950--2023
- **Unidad base:** Millones de dólares
- **Fuente original:**
  - 1960--2023: Banco Mundial, https://datos.bancomundial.org/indicador/FI.RES.TOTL.CD?locations=BO
  - 1950--1960: Informes del Banco Central de Bolivia (páginas específicas pendientes)
- **Notas:** Falta insertar detalles de informes y páginas exactas para 1950–1960.

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `reservas_totales` | REAL | Reservas totales en oro y divisas (millones USD) |

### 4. Procesamiento aplicado

Los datos originalmente estaban en unidades; se procesaron para convertirlos a millones de dólares.
## Venta de Divisas al Banco Central

(`venta_de_divisas_al_banco_central`)}
### 1. Listado

- **Nombre de tabla:** `venta_de_divisas_al_banco_central`
- **Nombre descriptivo:** Valor real de las exportaciones y divisas vendidas al BCB

### 2. Estructura

- **Descripción:** Serie anual que compara el valor real de las exportaciones bolivianas con las divisas efectivamente vendidas al Banco Central de Bolivia (BCB), para analizar la disponibilidad de liquidez externa y su canalización hacia las reservas internacionales.
- **Periodo:** 1947--1964
- **Unidad base:** Millones de dólares (USD)
- **Fuente original:**
  - 1947--1951: *Memoria del Banco Central de Bolivia, 1956*, págs. 69--71
  - 1952--1963: *Memoria del Banco Central de Bolivia, 1953*, págs. 117 y 141
  - 1964: *Memoria del Banco Central de Bolivia, 1954*, págs. 133 y 151
- **Notas:** El año base del deflactor para *exportaciones reales* no se especifica en la fuente original; se mantiene la denominación empleada en el cuadro.

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `exportaciones_reales` | REAL | Valor real de las exportaciones (USD constantes) |
| `divisas_vendidas` | REAL | Divisas vendidas al BCB (USD) |

### 4. Procesamiento aplicado

Ninguno.
# Exportaciones

## Exportaciones Totales (`exportaciones_totales`)

### 1. Listado

- **Nombre de tabla:** `exportaciones_totales`
- **Nombre descriptivo:** Valor total de exportaciones tradicionales y no tradicionales

### 2. Estructura

- **Descripción:** Registro anual de exportaciones desagregadas entre productos tradicionales y no tradicionales, junto con su valor total oficial.
- **Periodo:** 1980--2023
- **Unidad base:** Millones de dólares
- **Fuente original:**
  - 1980--1992: Archivo Excel `db/pruebas.xlsx`
  - 1992--2023: INE, https://nube.ine.gob.bo/index.php/s/zUQc65wIGkw1KUy/download
- **Notas:** En INE aparece como exportaciones por producto, tradicionales y no tradicionales.

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `productos_tradicionales` | REAL | Valor de exportaciones tradicionales (millones USD) |
| `productos_no_tradicionales` | REAL | Valor de exportaciones no tradicionales (millones USD) |
| `total_valor_oficial` | REAL | Suma oficial de todas las exportaciones (millones USD) |

### 4. Procesamiento aplicado

Ninguno.
## Volumen y Valor de Exportaciones de Minerales (`exportaciones_minerales_totales`)

### 1. Listado

- **Nombre de tabla:** `exportaciones_minerales_totales`
- **Nombre descriptivo:** Volumen y valor de exportaciones de minerales

### 2. Estructura

- **Descripción:** Registra anualmente el volumen (en kilos finos) y el valor (en miles de dólares) de las exportaciones de minerales para evaluar la evolución del sector minero.
- **Periodo:** 1952--2023
- **Unidad base:** Volumen en kilos finos; valor en miles de dólares
- **Fuente original:**
  - 1952--1987: Informes del Banco Central de Bolivia
  - 1987--2023: UDAPE, https://dossier.udape.gob.bo/res/VOLUMEN%20Y%20VALOR%20DE%20EXPORTACIONES%20DE%20MINERALES
- **Notas:** Datos preliminares para 2018--2023

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `estaño_volumen` | REAL | Volumen de estaño (kilos finos) |
| `estaño_valor` | REAL | Valor de estaño (miles USD) |
| `plomo_volumen` | REAL | Volumen de plomo (kilos finos) |
| `plomo_valor` | REAL | Valor de plomo (miles USD) |
| `zinc_volumen` | REAL | Volumen de zinc (kilos finos) |
| `zinc_valor` | REAL | Valor de zinc (miles USD) |
| `plata_volumen` | REAL | Volumen de plata (kilos finos) |
| `plata_valor` | REAL | Valor de plata (miles USD) |
| `wolfram_volumen` | REAL | Volumen de wólfram (kilos finos) |
| `wolfram_valor` | REAL | Valor de wólfram (miles USD) |
| `cobre_volumen` | REAL | Volumen de cobre (kilos finos) |
| `cobre_valor` | REAL | Valor de cobre (miles USD) |
| `antimonio_volumen` | REAL | Volumen de antimonio (kilos finos) |
| `antimonio_valor` | REAL | Valor de antimonio (miles USD) |
| `oro_volumen` | REAL | Volumen de oro (kilos finos) |
| `oro_valor` | REAL | Valor de oro (miles USD) |

### 4. Procesamiento aplicado

Ninguno.
## Exportaciones Tradicionales (`exportaciones_tradicionales`)

### 1. Listado

- **Nombre de tabla:** `exportaciones_tradicionales`
- **Nombre descriptivo:** Exportaciones tradicionales de minerales e hidrocarburos

### 2. Estructura

- **Descripción:** Registra el valor anual de las exportaciones tradicionales, desglosadas en minerales e hidrocarburos, para evaluar su participación en el comercio exterior.
- **Periodo:** 1992--2024
- **Unidad base:** Millones de dólares
- **Fuente original:** INE — https://www.ine.gob.bo/index.php/estadisticas-economicas/comercio-exterior/cuadros-estadisticos-exportaciones/
- **Notas:** Datos preliminares para 2023 y 2024

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `minerales` | REAL | Valor de exportaciones de minerales (millones USD) |
| `hidrocarburos` | REAL | Valor de exportaciones de hidrocarburos (millones USD) |

### 4. Procesamiento aplicado

Ninguno.
## Exportaciones Tradicionales y No Tradicionales

(`exportaciones_tradicionales_no_tradicionales`)}
### 1. Listado

- **Nombre de tabla:** `exportaciones_tradicionales_no_tradicionales`
- **Nombre descriptivo:** Desglose de exportaciones tradicionales y no tradicionales

### 2. Estructura

- **Descripción:** Valor anual de exportaciones divididas en categorías tradicionales y no tradicionales, para analizar su evolución y peso relativo.
- **Periodo:** 1980--2024
- **Unidad base:** Millones de dólares
- **Fuente original:** INE — https://www.ine.gob.bo/index.php/estadisticas-economicas/comercio-exterior/cuadros-estadisticos-exportaciones/
- **Notas:** Datos preliminares para 2023 y 2024

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `tradicionales` | REAL | Exportaciones tradicionales (millones USD) |
| `no_tradicionales` | REAL | Exportaciones no tradicionales (millones USD) |

### 4. Procesamiento aplicado

Ninguno.
## Participación de Exportaciones Tradicionales y No Tradicionales

(`participacion_exp_trad_no_trad`)}
### 1. Listado

- **Nombre de tabla:** `participacion_exp_trad_no_trad`
- **Nombre descriptivo:** Participación porcentual de exportaciones tradicionales y no tradicionales

### 2. Estructura

- **Descripción:** Porcentaje anual que representan las exportaciones tradicionales y no tradicionales sobre el total de exportaciones.
- **Periodo:** 1980--2023
- **Unidad base:** Porcentaje
- **Fuente original:** Archivo Excel `db/pruebas.xlsx`
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `exp_trad` | REAL | Exportaciones tradicionales (% del total) |
| `exp_no_trad` | REAL | Exportaciones no tradicionales (% del total) |

### 4. Procesamiento aplicado

Ninguno.
## Exportaciones Tradicionales de Hidrocarburos

(`exportaciones_tradicionales_hidrocarburos`)}
### 1. Listado

- **Nombre de tabla:** `exportaciones_tradicionales_hidrocarburos`
- **Nombre descriptivo:** Exportaciones de hidrocarburos, gas natural y otros hidrocarburos

### 2. Estructura

- **Descripción:** Valores anuales de exportaciones de hidrocarburos, desglosados en gas natural y otros hidrocarburos, para evaluar su contribución al comercio exterior.
- **Periodo:** 1992--2024
- **Unidad base:** Millones de dólares
- **Fuente original:** INE — https://www.ine.gob.bo/index.php/estadisticas-economicas/comercio-exterior/cuadros-estadisticos-exportaciones/
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `hidrocarburos` | REAL | Total hidrocarburos (millones USD) |
| `gas_natural` | REAL | Gas natural (millones USD) |
| `otros_hidrocarburos` | REAL | Otros hidrocarburos (millones USD) |

### 4. Procesamiento aplicado

Ninguno.
## Exportación de Gas Natural

(`exportacion_gas_natural`)}
### 1. Listado

- **Nombre de tabla:** `exportacion_gas_natural`
- **Nombre descriptivo:** Volumen, precio y valor de exportación de gas natural

### 2. Estructura

- **Descripción:** Porcentaje anual de volumen (MMmc y MMPC), precio (USD por MPC) y valor (miles de USD) de las exportaciones de gas natural.
- **Periodo:** 1987--2023
- **Unidad base:**
  - Volumen: Millones de metros cúbicos (MMmc) y Millones de pies cúbicos (MMPC)
  - Precio: Dólares por mil pie cúbico (USD/MPC)
  - Valor: Miles de dólares (miles USD)
- **Fuente original:** UDAPE https://dossier.udape.gob.bo/res/EXPORTACIÓN%20DE%20GAS%20NATURAL
- **Notas:** Datos preliminares para 2021–2023

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `volumen_MMMc` | REAL | Volumen en millones de metros cúbicos (MMmc) |
| `volumen_MMPC` | REAL | Volumen en millones de pies cúbicos (MMPC) |
| `precio_usd_MPC` | REAL | Precio en USD por mil pie cúbico (USD/MPC) |
| `valor` | REAL | Valor en miles de dólares |

### 4. Procesamiento aplicado

Ninguno.
## Exportación de Gas Natural por Contrato

(`exportacion_gas_natural_contratos`)}
### 1. Listado

- **Nombre de tabla:** `exportacion_gas_natural_contratos`
- **Nombre descriptivo:** Exportación de gas natural detallada por contrato

### 2. Estructura

- **Descripción:** Valor anual de exportación de gas natural desglosado por contrato y destino, para analizar obligaciones y volúmenes por mercado.
- **Periodo:** 1992--2023
- **Unidad base:** Millones de dólares
- **Fuente original:** https://dossier.udape.gob.bo/res/VALOR%20DE%20EXPORTACI%C3%93N%20DE%20GAS%20NATURAL%20POR%20CONTRATO
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `contrato` | TEXT | Nombre del contrato de exportación |
| `destino` | TEXT | Destino del gas (Argentina o Brasil) |
| `monto` | REAL | Valor exportado (millones USD) |

### 4. Procesamiento aplicado

Ninguno.
## Participación del Gas Natural y Otros Hidrocarburos en el Total de Exportaciones de Hidrocarburos

(`participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos`)}
### 1. Listado

- **Nombre de tabla:** `participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos`
- **Nombre descriptivo:** Participación porcentual del gas natural y otros hidrocarburos en el total exportado de hidrocarburos

### 2. Estructura

- **Descripción:** Porcentaje anual que representan las exportaciones de gas natural y de otros hidrocarburos sobre el total de exportaciones de hidrocarburos.
- **Periodo:** 1980--2023
- **Unidad base:** Porcentaje
- **Fuente original:** Archivo Excel `db/pruebas.xlsx`
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `exportacion_gas` | REAL | Gas natural (% del total de hidrocarburos) |
| `otros_hidrocarburos` | REAL | Otros hidrocarburos (% del total de hidrocarburos) |

### 4. Procesamiento aplicado

Ninguno.
subsection[Participación Hidrocarburos vs Minerales]{%
Participación de Hidrocarburos y Minerales en Exportaciones Tradicionales
{(`participacion_hidrocarburos_minerales_exportaciones_tradicionales`)}%
}
### 1. Listado

- **Nombre de tabla:** `participacion_hidrocarburos_minerales_exportaciones_tradicionales`
- **Nombre descriptivo:** Participación porcentual de hidrocarburos y minerales en exportaciones tradicionales

### 2. Estructura

- **Descripción:** Porcentaje anual que representan las exportaciones de hidrocarburos y de minerales dentro del total de exportaciones tradicionales.
- **Periodo:** 1980--2023
- **Unidad base:** Porcentaje
- **Fuente original:** Archivo Excel `db/pruebas.xlsx`
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `minerales` | REAL | Exportaciones de minerales (% del total tradicional) |
| `hidrocarburos` | REAL | Exportaciones de hidrocarburos (% del total tradicional) |

### 4. Procesamiento aplicado

Ninguno.
## Exportaciones No Tradicionales

### 1. Listado

- **Nombre de tabla:** `exportaciones_no_tradicionales`
- **Nombre descriptivo:** Exportaciones No Tradicionales de Bolivia

### 2. Estructura

- **Descripción:** Serie histórica anual de las exportaciones no tradicionales de Bolivia, desagregada por producto, en millones de dólares.
- **Periodo:** 1992--2024
- **Unidad base:** Millones de dólares
- **Fuente original:** https://www.ine.gob.bo/index.php/estadisticas-economicas/comercio-exterior/cuadros-estadisticos-exportaciones/
- **Notas:** 2023 y 2024 datos preliminares

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER PRIMARY KEY | Año del registro |
| `total` | REAL | Total exportaciones no tradicionales (millones de dólares) |
| `castaña` | REAL | Exportaciones de castaña |
| `café` | REAL | Exportaciones de café |
| `cacao` | REAL | Exportaciones de cacao |
| `azúcar` | REAL | Exportaciones de azúcar |
| `bebidas` | REAL | Exportaciones de bebidas |
| `gomas` | REAL | Exportaciones de gomas |
| `cueros` | REAL | Exportaciones de cueros |
| `maderas` | REAL | Exportaciones de maderas |
| `algodón` | REAL | Exportaciones de algodón |
| `soya` | REAL | Exportaciones de soya |
| `joyería` | REAL | Exportaciones de joyería |
| `joyería_con_oro_imp` | REAL | Exportaciones de joyería con oro importado |
| `otros` | REAL | Exportaciones de otros productos |

### 4. Procesamiento aplicado

Ninguno.
# Importaciones

## Composición de Importaciones por Uso y Destino

### 1. Listado

- **Nombre de tabla:** `composicion_importaciones_uso_destino`
- **Nombre descriptivo:** Distribución de importaciones según uso o destino económico

### 2. Estructura

- **Descripción:** Clasifica el valor anual de las importaciones por bienes de consumo, materias primas/productos intermedios, bienes de capital y otros usos, en valor CIF frontera.
- **Periodo:** 1980--2024
- **Unidad base:** Valor CIF frontera (millones de dólares)
- **Fuente original:**
  - 1980--1992: Archivo Excel `db/pruebas.xlsx`
  - 1992--2024: INE, https://www.ine.gob.bo/index.php/estadisticas-economicas/comercio-exterior/importaciones-cuadros-estadisticos/
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `bienes_consumo` | REAL | Bienes de consumo (millones USD) |
| `materias_primas_productos_intermedios` | REAL | Materias primas / productos intermedios (millones USD) |
| `bienes_capital` | REAL | Bienes de capital (millones USD) |
| `diversos` | REAL | Otros usos (millones USD) |
| `total_valor_oficial_cif` | REAL | Total valor oficial CIF (millones USD) |

### 4. Procesamiento aplicado

Ninguno.
## Participación de la Composición de Importaciones por Uso y Destino

### 1. Listado

- **Nombre de tabla:** `participacion_composicion_importaciones_uso_destino`
- **Nombre descriptivo:** Participación porcentual de categorías de importaciones sobre el total CIF

### 2. Estructura

- **Descripción:** Porcentaje anual de bienes de consumo, materias primas/productos intermedios, bienes de capital y otros usos en el total de importaciones valor CIF frontera.
- **Periodo:** 1980--2024
- **Unidad base:** Porcentaje
- **Fuente original:** Archivo Excel `db/pruebas.xlsx`
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `bienes_consumo` | REAL | Bienes de consumo (% del total CIF) |
| `materias_primas_productos_intermedios` | REAL | Materias primas/productos intermedios (% del total CIF) |
| `bienes_capital` | REAL | Bienes de capital (% del total CIF) |
| `diversos` | REAL | Otros usos (% del total CIF) |
| `total_cif` | REAL | Total importaciones CIF (porcentaje, siempre 100%) |

### 4. Procesamiento aplicado

Ninguno.
# Precios y Producción

## Precio real de minerales

### 1. Listado

- **Nombre de tabla:** `precio_minerales`
- **Nombre descriptivo:** Precios de minerales principales

### 2. Estructura

- **Descripción:** Precio anual de minerales principales expresado en USD según unidad de medida de cada columna.
- **Periodo:** 1980 a 2015
- **Unidad base:** USD
- **Fuente original:** MINISTRO DE MINERÍA Y METALURGIA: https://mineria.gob.bo/revista/pdf/20170817-10-15-28.pdf
- **Notas:** ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año del registro |
| Zinc | REAL | Precio del Zinc (Libras Finas -- L.F) |
| Estaño | REAL | Precio del Estaño (Libras Finas -- L.F) |
| Oro | REAL | Precio del Oro (Onzas Troy -- O.T.) |
| Plata | REAL | Precio de la Plata (Onzas Troy -- O.T.) |
| Antimonio | REAL | Precio del Antimonio (Toneladas Métricas) |
| Plomo | REAL | Precio del Plomo (Libras Finas -- L.F) |
| Wólfram | REAL | Precio del Wólfram (Libras Finas) |
| Cobre | REAL | Precio del Cobre (Libras Finas -- L.F) |

### 4. Procesamiento aplicado

Ninguno.
## Precios oficiales de minerales principales

### 1. Listado

- **Nombre de tabla:** `precio_oficial_minerales`
- **Nombre descriptivo:** Precios oficiales de minerales principales

### 2. Estructura

- **Descripción:** Precio oficial anual de minerales principales en USD.
- **Periodo:** 1950 a 2023
- **Unidad base:** USD
- **Fuente original:**
  - 1950–1980: Informes del Banco Central de Bolivia
  - 1980–2015: Ministerio de Minería y Metalurgia https://mineria.gob.bo/revista/pdf/20170817-10-15-28.pdf
  - 2015–2023: Ministerio de Minería y Metalurgia https://mineria.gob.bo/documentos/dossier_1980_2023.pdf small{(pendiente insertar referencias de página específicas)}
- **Notas:** ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Precio en USD por** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año del registro |
| zinc | REAL | libra fina (L.F.) |
| estaño | REAL | libra fina (L.F.) |
| oro | REAL | onza troy (O.T.) |
| plata | REAL | onza troy (O.T.) |
| antimonio | REAL | tonelada métrica fina (T.M.F.) |
| plomo | REAL | libra fina (L.F.) |
| wolfram | REAL | libra fina (U.L.F.) |
| cobre | REAL | libra fina (L.F.) |
| bismuto | REAL | libra fina (L.F.) |
| cadmio | REAL | libra fina (L.F.) |
| manganeso | REAL | libra fina (U.L.F.) |

### 4. Procesamiento aplicado

Ninguno.
## Precio internacional del petróleo WTI

### 1. Listado

- **Nombre de tabla:** `precio_petroleo_wti`
- **Nombre descriptivo:** Precio internacional del petróleo WTI

### 2. Estructura

- **Descripción:** Precio anual del petróleo WTI en dólares por barril.
- **Periodo:** 1996 a 2023
- **Unidad base:** Dólares por barril
- **Fuente original:** UDAPE: https://dossier.udape.gob.bo/res/PRECIO%20INTERNACIONAL%20DEL%20PETR%C3%93LEO%20(WTI)
- **Notas:** ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año del registro |
| precio | REAL | Precio del petróleo WTI (USD por barril) |

### 4. Procesamiento aplicado

Ninguno.
## Producción de minerales principales

### 1. Listado

- **Nombre de tabla:** `produccion_minerales`
- **Nombre descriptivo:** Producción de minerales principales

### 2. Estructura

- **Descripción:** Producción anual de minerales principales en toneladas finas.
- **Periodo:** 1985 a 2021
- **Unidad base:** Toneladas finas
- **Fuente original:** Ministerio de Minería y Metalurgia: https://mineria.gob.bo/revista/pdf/20170817-10-15-28.pdf
- **Notas:** ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año del registro |
| zinc | REAL | Producción de Zinc (toneladas finas) |
| estaño | REAL | Producción de Estaño (toneladas finas) |
| oro | REAL | Producción de Oro (toneladas finas) |
| plata | REAL | Producción de Plata (toneladas finas) |
| antimonio | REAL | Producción de Antimonio (toneladas finas) |
| plomo | REAL | Producción de Plomo (toneladas finas) |
| wolfram | REAL | Producción de Wólfram (toneladas finas) |
| cobre | REAL | Producción de Cobre (toneladas finas) |

### 4. Procesamiento aplicado

Se reconvirtieron algunas series para expresarlas en toneladas finas según especificación de fuente.
## Inflación acumulada

### 1. Listado

- **Nombre de tabla:** `inflacion_acumulada`
- **Nombre descriptivo:** Variación porcentual acumulada anual del Índice de Precios al Consumidor (Diciembre a diciembre)

### 2. Estructura

- **Descripción:** Serie histórica de la variación porcentual acumulada anual del IPC para Bolivia.
- **Periodo:** 1982–2024
- **Unidad base:** Porcentaje
- **Fuente original:**
  - Banco Central de Bolivia (1982–1992): `reports/inflacion_acumulada/`
  - INE (1993–2007): https://nube.ine.gob.bo/index.php/s/LzucAyViXN7ikbL/download
  - INE (2009–2017): https://nube.ine.gob.bo/index.php/s/kVGgyqtobYRsZwv/download
  - INE (2018–2024): https://nimbus.ine.gob.bo/index.php/s/KDwe4CYNtL4GPfq/download
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año calendario |
| inflacion | REAL | Variación porcentual acumulada (Diciembre a diciembre) |

### 4. Procesamiento aplicado

Ninguno.
## Cotización oficial del dólar

### 1. Listado

- **Nombre de tabla:** `cotizacion_oficial_dolar`
- **Nombre descriptivo:** Tipo de cambio oficial del dólar estadounidense

### 2. Estructura

- **Descripción:** Serie histórica del tipo de cambio oficial (compra y venta) del dólar estadounidense.
- **Periodo:** 1958–2023
- **Unidad base:** Bolivianos por dólar
- **Fuente original:** UDAPE – Cotización oficial del dólar: https://dossier.udape.gob.bo/res/COTIZACI%C3%93N%20MENSUAL%20OFICIAL%20Y%20PARALELA%20DEL%20D%C3%93LAR%20NORTEAMERICANO
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año de referencia |
| oficial_compra | REAL | Tipo de cambio oficial (compra) |
| oficial_venta | REAL | Tipo de cambio oficial (venta) |

### 4. Procesamiento aplicado

Ninguno.
## Poder Adquisitivo y Coste de la Vida

(`poder_adquisitivo_coste_vida`)}
### 1. Listado

- **Nombre de tabla:** `poder_adquisitivo_coste_vida`
- **Nombre descriptivo:** Poder adquisitivo de la población y coste de la vida

### 2. Estructura

- **Descripción:** Mide anualmente la liquidez disponible (efectivo,+,depósitos) en millones de bolivianos, junto con dos índices base 100 en 1951: uno de poder adquisitivo y otro de coste de la vida.
- **Periodo:** 1951--1964
- **Unidad base:**
  - Billetes, depósitos y poder adquisitivo: millones de bolivianos
  - Índices: base 100 = 1951
- **Fuente original:** *Memorias del Banco Central de Bolivia* (años 1956, 1963 y 1964)
  - 1951--1956 en “Memoria BCB, 1956” (pp.,69--71)
  - 1957--1963 en “Memoria BCB, 1963”
  - 1964 en “Memoria BCB, 1964” (pp.,133, 151)
- **Notas:** Se omiten las columnas de incremento anual.

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `billetes_publico` | REAL | Efectivo en poder del público (millones Bs) |
| `depositos_publico` | REAL | Depósitos a la vista del público (millones Bs) |
| `poder_adquisitivo` | REAL | Suma de billetes y depósitos (millones Bs) |
| `indice_poder_adquisitivo` | REAL | Índice de poder adquisitivo (base 100=1951) |
| `indice_coste_vida` | REAL | Índice de coste de la vida (base 100=1951) |

### 4. Procesamiento aplicado

Ninguno.
## Cotización del Dólar en Mercado Libre

(`cotizacion_dolar_mercado_libre`)}
### 1. Listado

- **Nombre de tabla:** `cotizacion_dolar_mercado_libre`
- **Nombre descriptivo:** Cotización del boliviano en relación al dólar (Mercado Libre)

### 2. Estructura

- **Descripción:** Valor anual de cuántos bolivianos cuesta un dólar estadounidense en el Mercado Libre al cierre de cada año (diciembre).
- **Periodo:** 1950--1960
- **Unidad base:** Bolivianos por dólar (Bs/USD)
- **Fuente original:** Banco Central de Bolivia — *El Trimestre Económico*, Cuadro 2

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro (diciembre) |
| `valor` | REAL | Cotización (Bs por USD) |

### 4. Procesamiento aplicado

Ninguno.
# Sector Fiscal

## Consolidado de operaciones del SPNF

### 1. Listado

- **Nombre de tabla:** `consolidado_spnf`
- **Nombre descriptivo:** Consolidado de operaciones del Sector Público No Financiero (SPNF)

### 2. Estructura

- **Descripción:** Operaciones consolidadas del SPNF: ingresos, egresos, superávit/deficit global y primario, y financiamiento.
- **Periodo:** 1990 a 2023
- **Unidad base:** Millones de bolivianos
- **Fuente original:** UDAPE: https://dossier.udape.gob.bo/res/operaciones%20consolidadas%20del%20sector
- **Notas:** ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año del registro |
| ingresos_totales | REAL | Ingresos totales del SPNF (Millones de BOB) |
| egresos_totales | REAL | Egresos totales del SPNF (Millones de BOB) |
| sup_o_def_global | REAL | Superávit o déficit global (Millones de BOB) |
| financiamiento | REAL | Financiamiento neto (Millones de BOB) |
| sup_o_def_primario | REAL | Superávit o déficit primario (Millones de BOB) |

### 4. Procesamiento aplicado

Ninguno.
## Operaciones de empresas públicas

### 1. Listado

- **Nombre de tabla:** `operaciones_empresas_publicas`
- **Nombre descriptivo:** Operaciones de empresas públicas

### 2. Estructura

- **Descripción:** Ingresos, egresos y resultado fiscal global de empresas públicas como porcentaje del PIB.
- **Periodo:** 1990 a 2020
- **Unidad base:** % del PIB
- **Fuente original:** Pendiente (Excel en USB)
- **Notas:** la fuente pendiente se encuentra en un Excel en el USB

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año del registro |
| ingresos_totales | REAL | Ingresos totales de empresas públicas (% PIB) |
| egresos_totales | REAL | Egresos totales de empresas públicas (% PIB) |
| resultado_fiscal_global | REAL | Resultado fiscal global (% PIB) |

### 4. Procesamiento aplicado

Ninguno.
## Inversión pública total

### 1. Listado

- **Nombre de tabla:** `inversion_publica_total`
- **Nombre descriptivo:** Inversión pública total

### 2. Estructura

- **Descripción:** Monto anual de la inversión pública total en miles de dólares.
- **Periodo:** 1990 a 2023
- **Unidad base:** Miles de dólares
- **Fuente original:** UDAPE: https://dossier.udape.gob.bo/res/INVERSI%C3%93N%20P%C3%9ABLICA%20POR%20SECTORES
- **Notas:** Datos preliminares desde 2018

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año del registro |
| valor | REAL NOT NULL | Inversión pública total (miles de USD) |

### 4. Procesamiento aplicado

Ninguno.
## Inversión pública por sectores

### 1. Listado

- **Nombre de tabla:** `inversion_publica_por_sectores`
- **Nombre descriptivo:** Inversión pública por sectores

### 2. Estructura

- **Descripción:** Distribución anual de la inversión pública entre sectores en miles de dólares.
- **Periodo:** 1990 a 2014
- **Unidad base:** Miles de dólares
- **Fuente original:** UDAPE: https://dossier.udape.gob.bo/res/INVERSI%C3%93N%20P%C3%9ABLICA%20POR%20SECTORES
- **Notas:** No se agregaron registros posteriores a 2014, pues la estructura de columnas cambia drásticamente.

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año del registro |
| extractivo | REAL | Inversión en sector extractivo (miles de USD) |
| apoyo_a_la_produccion | REAL | Inversión en apoyo a la producción (miles de USD) |
| infraestructura | REAL | Inversión en infraestructura (miles de USD) |
| sociales | REAL | Inversión en sector social (miles de USD) |
| total | REAL | Inversión pública total (miles de USD) |

### 4. Procesamiento aplicado

Ninguno.
## Ingresos Nacionales

### 1. Listado

- **Nombre de tabla:** `ingresos_nacionales`
- **Nombre descriptivo:** Ingresos Nacionales

### 2. Estructura

- **Descripción:** Totales anuales de transferencias estatales: coparticipación tributaria, IDH, HIPC II, regalías departamentales e IEHD.
- **Periodo:** 2001–2023 (proyecciones 2020(p)–2023(p))
- **Unidad base:** Millones de bolivianos
- **Fuente original:** UDAPE – Dossier: Ingresos por IDH, IEHD, regalías, coparticipación y HIPC II: https://dossier.udape.gob.bo/res/BOLIVIA%20RESUMEN:%20INGRESOS%20POR%20IDH,%20IEHD,%20REGALÍAS,%20COPARTICIPACIÓN%20Y%20HIPC%20II
- **Notas:** Los sufijos “(p)” indican datos preliminares o proyectados.

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año |
| ingresos_nacionales_total | REAL | Total ingresos |
| total_copart_tributaria | REAL | Copart. tributaria |
| total_idh | REAL | IDH total |
| total_hipc_ii | REAL | HIPC II |
| total_regalias_depart | REAL | Regalías dept. |
| total_iehd | REAL | IEHD |

### 4. Procesamiento aplicado

- Uniformización de nombres de columnas y manejo de indicadores preliminares “(p)”.

## Ingresos Corrientes

### 1. Listado

- **Nombre de tabla:** `ingresos_corrientes`
- **Nombre descriptivo:** Ingresos corrientes del SPNF

### 2. Estructura

- **Descripción:** Desagregación de los ingresos corrientes del Sector Público No Financiero en ingresos tributarios e impuestos sobre hidrocarburos, con su total.
- **Periodo:** 1990–2023 (proyecciones 2019(p)–2023(p))
- **Unidad base:** Millones de bolivianos
- **Fuente original:** UDAPE – Consolidado de operaciones del SPNF: https://dossier.udape.gob.bo/res/operaciones%20consolidadas%20del%20sector
- **Notas:** Los sufijos “(p)” indican datos preliminares o proyectados.

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año del registro |
| ingresos_tributarios | REAL | Ingresos tributarios del SPNF (Millones de BOB) |
| ingresos_hidrocarburos | REAL | Impuestos directos a los hidrocarburos (Millones de BOB) |
| total_ingresos_corrientes | REAL | Suma de ingresos tributarios e hidrocarburos (Millones de BOB) |

### 4. Procesamiento aplicado

- Extracción y limpieza de los datos originales de UDAPE.
- Conversión de comas miles a puntos decimales para tipo `REAL`.
- Cálculo explícito de la columna `total_ingresos_corrientes`.

## Ingresos Tributarios

### 1. Listado

- **Nombre de tabla:** `ingresos_tributarios`
- **Nombre descriptivo:** Ingresos tributarios del SPNF

### 2. Estructura

- **Descripción:** Desglose de los ingresos tributarios del Sector Público No Financiero en renta interna, renta aduanera y regalías mineras, con su total consolidado.
- **Periodo:** 1990–2023 (proyecciones 2019(p)–2023(p))
- **Unidad base:** Millones de bolivianos
- **Fuente original:** UDAPE – Consolidado de operaciones del SPNF: https://dossier.udape.gob.bo/res/operaciones%20consolidadas%20del%20sector UDAPE-Bolivia resumen: ingresos por idh, iehd, regalías, coparticipación y hipc II: https://dossier.udape.gob.bo/res/BOLIVIA%20RESUMEN:%20INGRESOS%20POR%20IDH,%20IEHD,%20REGALÍAS,%20COPARTICIPACIÓN%20Y%20HIPC%20II
- **Notas:** Los sufijos “(p)” indican datos preliminares o proyectados. La columna impuesto_directo_hidrocarburos fue extraida de bolivia resumen: ingresos por idh 

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PK | Año del registro |
| renta_interna | REAL | Renta interna (Millones de BOB) |
| renta_aduanera | REAL | Renta aduanera (Millones de BOB) |
| regalias_mineras | REAL | Regalías mineras (Millones de BOB) |
| impuesto_directo_hidrocarburos | REAL | IDH (Millones de BOB) |
| ingresos_tributarios_total | REAL | (Millones de BOB) |

### 4. Procesamiento aplicado

- Limpieza de separadores de miles (coma → punto decimal).
- Cálculo y verificación de la columna `ingresos_tributarios_total` como suma de los componentes.

## Ingresos por Hidrocarburos

### 1. Listado

- **Nombre de tabla:** `ingresos_hidrocarburos`
- **Nombre descriptivo:** Ingresos por hidrocarburos (IDH, IEHD y Regalías)

### 2. Estructura

- **Descripción:** Desglose anual de los ingresos fiscales provenientes del sector hidrocarburos: Impuesto Directo a los Hidrocarburos (IDH), Impuesto Especial a los Hidrocarburos y Derivados (IEHD) y regalías, junto con su total consolidado.
- **Periodo:** 1996–2023 (proyecciones 2019(p)–2023(p))
- **Unidad base:** Millones de bolivianos
- **Fuente original:** UDAPE – Consolidado de operaciones del SPNF: https://dossier.udape.gob.bo/res/operaciones%20consolidadas%20del%20sector
- **Notas:**
  1. Desde junio de 2005 se recauda el Impuesto Directo a los Hidrocarburos (IDH) según la Nueva Ley de Hidrocarburos.
  2. Los sufijos “(p)” indican datos preliminares o proyectados.

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año del registro |
| idh | REAL | Impuesto Directo a los Hidrocarburos (Millones BOB) |
| iehd | REAL | Impuesto Especial a los Hidrocarburos y Derivados (Millones BOB) |
| regalias | REAL | Regalías sobre hidrocarburos (Millones BOB) |
| ingresos_hidrocarburos_total | REAL | Total ingresos por hidrocarburos (Millones BOB) |

### 4. Procesamiento aplicado

- Conversión de valores a formato numérico (`REAL`), eliminando separadores de miles.
- Cálculo de `ingresos_hidrocarburos_total` como suma de IDH, IEHD y regalías.
- Marcado de filas preliminares “(p)” de acuerdo con la fuente.

## Evolución de las Finanzas Públicas

(`finanzas_publicas`)}
### 1. Listado

- **Nombre de tabla:** `finanzas_publicas`
- **Nombre descriptivo:** Evolución de recaudaciones, egresos y déficit fiscal

### 2. Estructura

- **Descripción:** Registra anualmente los ingresos fiscales totales, los egresos fiscales, el déficit (o superávit), y su conversión a dólares junto al tipo de cambio oficial al cierre de cada año.
- **Periodo:** 1947--1964
- **Unidad base:**
  - Ingresos, egresos y déficit: millones de bolivianos (Bs)
  - Conversión del déficit a USD: millones de dólares (USD)
  - Cotización del dólar: bolivianos por dólar (Bs/USD)
- **Fuente original:** *Memoria del Banco Central de Bolivia*, ediciones 1956, 1963 y 1964
  - 1947–1953: “Memoria BCB, 1956”, pág. 78
  - 1954–1960: “Memoria BCB, 1963”
  - 1961–1964: “Memoria BCB, 1964”, págs. 160–162
- **Notas:**
  - El signo negativo en `deficit` y `conversion_deficit_usd` indica déficit; sin signo.

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| `año` | INTEGER | Año del registro |
| `ingresos_fiscales` | REAL | Recaudaciones fiscales totales (millones Bs) |
| `egresos_fiscales` | REAL | Gasto público total (millones Bs) |
| `deficit` | REAL | Déficit (negativo) o superávit (positivo) en Bs |
| `conversion_deficit_usd` | REAL | Déficit/superávit convertido a USD (millones USD) |
| `cotizacion_dolar` | REAL | Tipo de cambio oficial (Bs por USD al 31-XII) |

### 4. Procesamiento aplicado

Ninguno.
# Deuda

## Deuda externa total

### 1. Listado

- **Nombre de tabla:** `deuda_externa_total`
- **Nombre descriptivo:** Deuda externa total

### 2. Estructura

- **Descripción:** Monto anual de la deuda externa total de Bolivia.
- **Periodo:** 1951 a 2024
- **Unidad base:** Millones de dólares
- **Fuente original:**
  - 1951-1989: Memorias del banco central
  - 1990–2018: UDAPE https://dossier.udape.gob.bo/res/DEUDA%20P%C3%9ABLICA%20EXTERNA%20DE%20MEDIANO
  - 2019–2024: Banco Central de Bolivia: Deuda externa pública por acreedor https://www.bcb.gob.bo/webdocs/publicacionesbcb/2025/06/36/%C3%8Dndice%20Boletin%20del%20Sector%20Externo%202024.pdf
- **Notas:**
  - Para 2020: No considera el instrumento de Financiamiento Rápido (IFR) del FMI debido a que esta operación vulneró los procedimientos establecidos en la Constitución Política del Estado para la contratación de deuda pública externa (artículo 158 y 322).
  - Desde 2022 hasta 2024: Datos preliminares.

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año del registro |
| deuda | REAL | Deuda externa total (Millones de USD) |

### 4. Procesamiento aplicado

Ninguno.
## Deuda interna pública

### 1. Listado

- **Nombre de tabla:** `deuda_interna`
- **Nombre descriptivo:** Stock de deuda interna del Tesoro General de la Nación

### 2. Estructura

- **Descripción:** Valor anual del stock de deuda interna manejada por el Tesoro General de la Nación.
- **Periodo:** 1993 a 2022
- **Unidad base:** Millones de dólares
- **Fuente original:** UDAPE: https://dossier.udape.gob.bo/res/STOCK%20DE%20LA%20DEUDA%20P%C3%9ABLICA%20INTERNA%20DEL%20TESORO%20GENERAL%20DE%20LA%20NACI%C3%93N
- **Notas:** ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año del registro |
| valor | REAL NOT NULL | Stock de deuda interna (Millones de USD) |

### 4. Procesamiento aplicado

Ninguno.
# Empleo

## Mercado laboral

### 1. Listado

- **Nombre de tabla:** `mercado_laboral`
- **Nombre descriptivo:** Indicadores del mercado laboral

### 2. Estructura

- **Descripción:** Serie anual de principales indicadores del mercado laboral en Bolivia.
- **Periodo:** 1999–2017
- **Unidad base:** Personas
- **Fuente original:** INE – Empleo: https://nube.ine.gob.bo/index.php/s/9nY0sTnKJK42cDM/download
- **Notas:** Ninguna

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción** |
|---|---|---|
| año | INTEGER PRIMARY KEY | Año de referencia |
| total_poblacion | INTEGER | Población total (todas las personas) |
| pent | INTEGER | Población en Edad de No Trabajar (PENT) |
| pet | INTEGER | Población en Edad de Trabajar (PET) |
| pea | INTEGER | Población Económicamente Activa (PEA) |
| po | INTEGER | Ocupados |
| pd | INTEGER | Desocupados |
| cesantes | INTEGER | Cesantes |
| aspirantes | INTEGER | Aspirantes |
| pei | INTEGER | Población Económicamente Inactiva (PEI) |
| temporales | INTEGER | Inactivos temporales |
| permanentes | INTEGER | Inactivos permanentes |

### 4. Procesamiento aplicado

Ninguno.
# Pobreza

## Pobreza (`pobreza`)

### 1. Listado

- **Nombre de tabla:** `pobreza`
- **Nombre descriptivo:** Indicadores de pobreza (FGT) y población por ámbito (Bolivia, urbano, rural)

### 2. Estructura

- **Descripción:** Serie anual de indicadores Foster–Greer–Thorbecke (FGT0 incidencia, FGT1 brecha, FGT2 severidad) y tamaños poblacionales total y pobre, reportados para el total nacional (Bolivia), área urbana y área rural.
- **Periodo:** 2005--2023
- **Unidad base:**
  - **FGT0/FGT1/FGT2:** Porcentaje (%).
  - **Población total / Población pobre:** Personas.
- **Fuente original:** INE – Encuestas de Hogares: https://www.ine.gob.bo/index.php/estadisticas-economicas/encuestas-de-hogares/
- **Notas:**
  1. FGT0: incidencia (proporción de personas en pobreza); FGT1: brecha promedio respecto a la línea de pobreza; FGT2: severidad (pondera más las brechas grandes).
  2. FGT en % (0–100). `pop_poor_*` $leq$ `pop_total_*`.
  3. en el excel original no se proporcionan datos para 2010

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción / Unidad** |
|---|---|---|
| `año` | INTEGER PRIMARY KEY | Año del registro |
| `fgt0_bol` | REAL | Incidencia de pobreza (FGT0), Bolivia [%] |
| `fgt1_bol` | REAL | Brecha de pobreza (FGT1), Bolivia [%] |
| `fgt2_bol` | REAL | Severidad de pobreza (FGT2), Bolivia [%] |
| `pop_total_bol` | INTEGER | Población total, Bolivia [personas] |
| `pop_poor_bol` | INTEGER | Población en pobreza, Bolivia [personas] |
| `fgt0_urb` | REAL | Incidencia de pobreza (FGT0), Urbano [%] |
| `fgt1_urb` | REAL | Brecha de pobreza (FGT1), Urbano [%] |
| `fgt2_urb` | REAL | Severidad de pobreza (FGT2), Urbano [%] |
| `pop_total_urb` | INTEGER | Población total, Urbano [personas] |
| `pop_poor_urb` | INTEGER | Población en pobreza, Urbano [personas] |
| `fgt0_rur` | REAL | Incidencia de pobreza (FGT0), Rural [%] |
| `fgt1_rur` | REAL | Brecha de pobreza (FGT1), Rural [%] |
| `fgt2_rur` | REAL | Severidad de pobreza (FGT2), Rural [%] |
| `pop_total_rur` | INTEGER | Población total, Rural [personas] |
| `pop_poor_rur` | INTEGER | Población en pobreza, Rural [personas] |

### 4. Procesamiento aplicado

Ninguna
## Pobreza extrema (`pobreza_extrema`)

### 1. Listado

- **Nombre de tabla:** `pobreza_extrema`
- **Nombre descriptivo:** Indicadores de pobreza extrema (FGT) y población por ámbito (Bolivia, urbano, rural)

### 2. Estructura

- **Descripción:** Serie anual de indicadores Foster--Greer--Thorbecke para *pobreza extrema*: FGT0 (incidencia), FGT1 (brecha) y FGT2 (severidad), junto con población total y población en pobreza extrema, para el total nacional (Bolivia), área urbana y área rural.
- **Periodo:** 2005--2023
- **Unidad base:**
  - **FGT0/FGT1/FGT2:** Porcentaje (%).
  - **Población total / Población en pobreza extrema:** Personas.
- **Fuente original:** INE -- Encuestas de Hogares:; https://www.ine.gob.bo/index.php/estadisticas-economicas/encuestas-de-hogares/
- **Notas:**
  1. FGT0: proporción de personas en pobreza extrema; FGT1: brecha promedio respecto a la línea de pobreza extrema; FGT2: severidad (mayor peso a brechas grandes).
  2. Los indicadores FGT se expresan en el rango 0--100,%.
  3. Para 2010 no existe dato oficial reportado por INE; el registro se deja nulo y se documenta la discontinuidad.

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción / Unidad** |
|---|---|---|
| `año` | INTEGER PRIMARY KEY | Año del registro |
| `fgt0_urb` | REAL | Incidencia de pobreza extrema (FGT0), Urbano [%] |
| `fgt1_urb` | REAL | Brecha de pobreza extrema (FGT1), Urbano [%] |
| `fgt2_urb` | REAL | Severidad de pobreza extrema (FGT2), Urbano [%] |
| `pop_total_urb` | INTEGER | Población total, Urbano [personas] |
| `pop_extreme_urb` | INTEGER | Población en pobreza extrema, Urbano [personas] |
| `fgt0_rur` | REAL | Incidencia de pobreza extrema (FGT0), Rural [%] |
| `fgt1_rur` | REAL | Brecha de pobreza extrema (FGT1), Rural [%] |
| `fgt2_rur` | REAL | Severidad de pobreza extrema (FGT2), Rural [%] |
| `pop_total_rur` | INTEGER | Población total, Rural [personas] |
| `pop_extreme_rur` | INTEGER | Población en pobreza extrema, Rural [personas] |
| `fgt0_bol` | REAL | Incidencia de pobreza extrema (FGT0), Bolivia [%] |
| `fgt1_bol` | REAL | Brecha de pobreza extrema (FGT1), Bolivia [%] |
| `fgt2_bol` | REAL | Severidad de pobreza extrema (FGT2), Bolivia [%] |
| `pop_total_bol` | INTEGER | Población total, Bolivia [personas] |
| `pop_extreme_bol` | INTEGER | Población en pobreza extrema, Bolivia [personas] |

### 4. Procesamiento aplicado

Ninguna
# Sector Monetario

## Agregados monetarios y emisión (`agregados_monetarios`)

### 1. Listado

- **Nombre de tabla:** `agregados_monetarios`
- **Nombre descriptivo:** Agregados monetarios (M0, M1, M2, M3) y emisión monetaria

### 2. Estructura

- **Descripción:** Serie anual de la base monetaria (M0), agregados monetarios (M1, M2, M3) y emisión monetaria para Bolivia. Los valores son niveles (stocks) anuales.
- **Periodo:**
  - Agregados monetarios y emisión monetaria: 1980--2022
  - M0, M1, M2 y M3: 1990--2022
- **Unidad base:** Miles de bolivianos (BOB).
- **Fuente original:** UDAPE — Dossier Monetaria:
  - *Base monetaria por origen y destino*
  - *Variables monetarias*
  - https://dossier.udape.gob.bo/res/monetaria
- **Notas:**
  - Donde no existe dato oficial, el registro se deja en `NULL` (p.,ej., M1--M3 antes de 1990).
  - Definiciones operativas: $M0=B=C+R$; $M1=C+D$; $M2=M1+F$; $M3=M2+G$; *Emisión* $E=C+CB$.
  - Series construidas con promedios anuales (renglón *PROMEDIO* en las tablas mensuales UDAPE/BCB).

### 3. Esquema de la tabla

| **Columna** | **Tipo** | **Descripción / Unidad** |
|---|---|---|
| `año` | REAL | Año del registro (AAAA) |
| `m0` | REAL | Base monetaria, miles de BOB |
| `m1` | REAL | Agregado M1, miles de BOB |
| `m2` | REAL | Agregado M2, miles de BOB |
| `m3` | REAL | Agregado M3, miles de BOB |
| `emision_monetaria` | REAL | Emisión monetaria ($E$), miles de BOB |

### 4. Procesamiento aplicado

- Extracción desde tablas UDAPE; selección del renglón *PROMEDIO* anual.
- Limpieza de separadores de miles y conversión a numérico.
- Alineación por año; inserción de `NULL` en ausencias (especialmente M1--M3 antes de 1990).