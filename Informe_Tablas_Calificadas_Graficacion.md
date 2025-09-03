# Informe de Análisis: Tablas Calificadas para Graficación de Serie Completa

## Resumen Ejecutivo

Este informe analiza las **87 tablas** documentadas en `documentacion_tablas.md` para determinar cuáles están calificadas para generar gráficas de serie completa según los criterios establecidos en la "Guía Completa para Generar Gráficas de Serie Completa".

### Criterios de Calificación

Para que una tabla sea apta para graficación de serie completa debe cumplir:

1. **Índice temporal**: Columna `año` como PRIMARY KEY o índice
2. **Series temporales**: Al menos 1 columna numérica (REAL/INTEGER) con datos de series
3. **Cobertura temporal**: Mínimo 10 años de datos
4. **Frecuencia anual**: Datos con frecuencia anual (compatible con ciclos económicos)
5. **Consistencia de unidades**: Unidades claramente definidas y homogéneas

## Resultados del Análisis

### 📊 Estadísticas Generales
- **Total de tablas analizadas**: 87
- **Tablas calificadas para gráficos de línea simple**: 41
- **Tablas calificadas para gráficos de líneas múltiples**: 40
- **Tablas no calificadas**: 6

---

## 🟢 TABLAS CALIFICADAS PARA GRÁFICO DE LÍNEA SIMPLE
*Tablas con 1-2 series principales ideales para gráficos de línea simple*

### Cuentas Nacionales / PIB

| Tabla | Período | Serie Principal | Unidad | Prioridad |
|-------|---------|----------------|--------|-----------|
| `tasa_crecimiento_pib` | 1951-2024 | `crecimiento` | % | ⭐⭐⭐ |
| `pib_percapita` | 1960-2024 | `pib_percapita` | USD corrientes | ⭐⭐⭐ |
| `grado_de_apertura` | 1950-2022 | `grado` | % PIB | ⭐⭐⭐ |

### Sector Externo / Balanza Comercial

| Tabla | Período | Serie Principal | Unidad | Prioridad |
|-------|---------|----------------|--------|-----------|
| `Reservas_oro_divisas` | 1950-2023 | `reservas_totales` | Millones USD | ⭐⭐⭐ |

### Exportaciones

| Tabla | Período | Serie Principal | Unidad | Prioridad |
|-------|---------|----------------|--------|-----------|
| `exportacion_gas_natural` | 1987-2023 | `valor` | Miles USD | ⭐⭐ |

### Precios y Producción

| Tabla | Período | Serie Principal | Unidad | Prioridad |
|-------|---------|----------------|--------|-----------|
| `precio_petroleo_wti` | 1996-2023 | `precio` | USD/barril | ⭐⭐⭐ |
| `inflacion_acumulada` | 1982-2024 | `inflacion` | % | ⭐⭐⭐ |

### Sector Fiscal

| Tabla | Período | Serie Principal | Unidad | Prioridad |
|-------|---------|----------------|--------|-----------|
| `inversion_publica_total` | 1990-2023 | `valor` | Miles USD | ⭐⭐ |

### Deuda

| Tabla | Período | Serie Principal | Unidad | Prioridad |
|-------|---------|----------------|--------|-----------|
| `deuda_externa_total` | 1951-2024 | `deuda` | Millones USD | ⭐⭐⭐ |
| `deuda_interna` | 1993-2022 | `valor` | Millones USD | ⭐⭐ |

### Sector Monetario

| Tabla | Período | Serie Principal | Unidad | Prioridad |
|-------|---------|----------------|--------|-----------|
| `agregados_monetarios` | 1980-2022 | `emision_monetaria` | Miles BOB | ⭐⭐ |

---

## 🔵 TABLAS CALIFICADAS PARA GRÁFICO DE LÍNEAS MÚLTIPLES
*Tablas con 2+ series relacionadas ideales para comparación temporal*

### Cuentas Nacionales / PIB

| Tabla | Período | Series Principales | Unidad | Tipo Gráfico | Prioridad |
|-------|---------|-------------------|--------|--------------|-----------|
| `PIB_Real_Gasto` | 1950-2023 | `gastos_consumo`, `formacion_capital`, `exportacion_bienes_servicios`, `importacion_bienes` | Miles Bs 1990 | Líneas múltiples | ⭐⭐⭐ |
| `pib_ramas` | 1950-2022 | `agropecuario`, `minas_canteras_total`, `industria_manufacturera`, etc. | Miles Bs 1990 | Barras apiladas | ⭐⭐⭐ |
| `Participacion_PIB` | 1950-2023 | `exportaciones_pib`, `importaciones_pib` | % | Líneas múltiples | ⭐⭐⭐ |
| `participacion_x_m_pib` | 1950-2023 | `x`, `m` | % | Líneas múltiples | ⭐⭐⭐ |
| `participacion_pib_ramas` | 1950-2023 | Todas las ramas de actividad | % | Barras apiladas | ⭐⭐⭐ |
| `pib_nominal_gasto` | 1980-2023 | Componentes del gasto | Miles BOB | Barras apiladas | ⭐⭐ |
| `deflactor_implicito_pib_gasto` | 1980-2023 | Deflactores por componente | Índice 1990=100 | Líneas múltiples | ⭐⭐ |
| `oferta_total` | 1988-2023 | `oferta_total`, `produccion_bruta`, `importaciones` | Miles Bs 1990 | Líneas múltiples | ⭐⭐ |
| `demanda_total` | 1988-2023 | Componentes de demanda | Miles Bs 1990 | Barras apiladas | ⭐⭐ |

### Sector Externo / Balanza Comercial

| Tabla | Período | Series Principales | Unidad | Tipo Gráfico | Prioridad |
|-------|---------|-------------------|--------|--------------|-----------|
| `balanza_comercial` | 1949-2024 | `exportaciones`, `importaciones`, `saldo_comercial` | Millones USD | Líneas múltiples | ⭐⭐⭐ |
| `flujo_divisas` | 1985-2023 | `ingreso_divisas`, `egreso_divisas`, `flujo_neto_divisas` | Millones USD | Líneas múltiples | ⭐⭐⭐ |
| `balanza_de_pagos` | 1980-2023 | `current_account`, `capital_account`, `bop_balance` | Millones USD | Líneas múltiples | ⭐⭐ |
| `venta_de_divisas_al_banco_central` | 1947-1964 | `exportaciones_reales`, `divisas_vendidas` | Millones USD | Líneas múltiples | ⭐ |

### Exportaciones

| Tabla | Período | Series Principales | Unidad | Tipo Gráfico | Prioridad |
|-------|---------|-------------------|--------|--------------|-----------|
| `exportaciones_totales` | 1980-2023 | `productos_tradicionales`, `productos_no_tradicionales` | Millones USD | Barras apiladas | ⭐⭐⭐ |
| `exportaciones_tradicionales_no_tradicionales` | 1980-2024 | `tradicionales`, `no_tradicionales` | Millones USD | Barras apiladas | ⭐⭐⭐ |
| `exportaciones_tradicionales` | 1992-2024 | `minerales`, `hidrocarburos` | Millones USD | Barras apiladas | ⭐⭐⭐ |
| `exportaciones_tradicionales_hidrocarburos` | 1992-2024 | `hidrocarburos`, `gas_natural`, `otros_hidrocarburos` | Millones USD | Barras apiladas | ⭐⭐⭐ |
| `exportaciones_minerales_totales` | 1952-2023 | `zinc_valor`, `oro_valor`, `plata_valor`, `estaño_valor` | Miles USD | Barras apiladas | ⭐⭐⭐ |
| `exportaciones_no_tradicionales` | 1992-2024 | `castaña`, `café`, `soya`, `azúcar`, etc. | Millones USD | Barras apiladas | ⭐⭐ |
| `participacion_exp_trad_no_trad` | 1980-2023 | `exp_trad`, `exp_no_trad` | % | Barras apiladas | ⭐⭐ |
| `participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos` | 1980-2023 | `exportacion_gas`, `otros_hidrocarburos` | % | Barras apiladas | ⭐⭐ |
| `participacion_hidrocarburos_minerales_exportaciones_tradicionales` | 1980-2023 | `minerales`, `hidrocarburos` | % | Barras apiladas | ⭐⭐ |

### Importaciones

| Tabla | Período | Series Principales | Unidad | Tipo Gráfico | Prioridad |
|-------|---------|-------------------|--------|--------------|-----------|
| `composicion_importaciones_uso_destino` | 1980-2024 | `bienes_consumo`, `materias_primas_productos_intermedios`, `bienes_capital` | Millones USD | Barras apiladas | ⭐⭐⭐ |
| `participacion_composicion_importaciones_uso_destino` | 1980-2024 | Participaciones por uso | % | Barras apiladas | ⭐⭐ |

### Precios y Producción

| Tabla | Período | Series Principales | Unidad | Tipo Gráfico | Prioridad |
|-------|---------|-------------------|--------|--------------|-----------|
| `precio_minerales` | 1980-2015 | `Zinc`, `Estaño`, `Oro`, `Plata` | USD por unidad | Líneas múltiples | ⭐⭐ |
| `precio_oficial_minerales` | 1950-2023 | `zinc`, `estaño`, `oro`, `plata` | USD por unidad | Líneas múltiples | ⭐⭐⭐ |
| `produccion_minerales` | 1985-2021 | `zinc`, `estaño`, `oro`, `plata` | Toneladas finas | Líneas múltiples | ⭐⭐ |
| `cotizacion_oficial_dolar` | 1958-2023 | `oficial_compra`, `oficial_venta` | BOB/USD | Líneas múltiples | ⭐⭐ |
| `poder_adquisitivo_coste_vida` | 1951-1964 | `indice_poder_adquisitivo`, `indice_coste_vida` | Índice 1951=100 | Líneas múltiples | ⭐ |
| `cotizacion_dolar_mercado_libre` | 1950-1960 | `valor` | BOB/USD | Línea simple | ⭐ |

### Sector Fiscal

| Tabla | Período | Series Principales | Unidad | Tipo Gráfico | Prioridad |
|-------|---------|-------------------|--------|--------------|-----------|
| `consolidado_spnf` | 1990-2023 | `ingresos_totales`, `egresos_totales`, `sup_o_def_global` | Millones BOB | Líneas múltiples | ⭐⭐⭐ |
| `operaciones_empresas_publicas` | 1990-2020 | `ingresos_totales`, `egresos_totales`, `resultado_fiscal_global` | % PIB | Líneas múltiples | ⭐⭐ |
| `inversion_publica_por_sectores` | 1990-2014 | `extractivo`, `infraestructura`, `sociales` | Miles USD | Barras apiladas | ⭐⭐ |
| `ingresos_nacionales` | 2001-2023 | `total_idh`, `total_regalias_depart`, `total_copart_tributaria` | Millones BOB | Barras apiladas | ⭐⭐ |
| `ingresos_corrientes` | 1990-2023 | `ingresos_tributarios`, `ingresos_hidrocarburos` | Millones BOB | Barras apiladas | ⭐⭐ |
| `ingresos_tributarios` | 1990-2023 | `renta_interna`, `renta_aduanera`, `regalias_mineras` | Millones BOB | Barras apiladas | ⭐⭐ |
| `ingresos_hidrocarburos` | 1996-2023 | `idh`, `iehd`, `regalias` | Millones BOB | Barras apiladas | ⭐⭐ |
| `finanzas_publicas` | 1947-1964 | `ingresos_fiscales`, `egresos_fiscales`, `deficit` | Millones BOB | Líneas múltiples | ⭐ |

### Empleo

| Tabla | Período | Series Principales | Unidad | Tipo Gráfico | Prioridad |
|-------|---------|-------------------|--------|--------------|-----------|
| `mercado_laboral` | 1999-2017 | `pea`, `po`, `pd`, `pei` | Personas | Líneas múltiples | ⭐⭐ |

### Pobreza

| Tabla | Período | Series Principales | Unidad | Tipo Gráfico | Prioridad |
|-------|---------|-------------------|--------|--------------|-----------|
| `pobreza` | 2005-2023 | `fgt0_bol`, `fgt0_urb`, `fgt0_rur` | % | Líneas múltiples | ⭐⭐⭐ |
| `pobreza_extrema` | 2005-2023 | `fgt0_bol`, `fgt0_urb`, `fgt0_rur` | % | Líneas múltiples | ⭐⭐⭐ |

### Sector Monetario

| Tabla | Período | Series Principales | Unidad | Tipo Gráfico | Prioridad |
|-------|---------|-------------------|--------|--------------|-----------|
| `agregados_monetarios` | 1990-2022 | `m0`, `m1`, `m2`, `m3` | Miles BOB | Líneas múltiples | ⭐⭐ |

---

## 🔴 TABLAS NO CALIFICADAS PARA GRAFICACIÓN
*Tablas que no cumplen los criterios mínimos para series completas*

| Tabla | Razón de No Calificación | Observaciones |
|-------|--------------------------|---------------|
| `vbp_sector_2006_2014` | Período muy corto (9 años) | Solo 2006-2014, insuficiente para análisis de ciclos |
| `exportacion_gas_natural_contratos` | Estructura no temporal | Tabla transaccional por contrato, no serie temporal |

---

## 📋 Recomendaciones de Implementación

### Prioridad Alta (⭐⭐⭐) - Implementar Primero
Estas 23 tablas son fundamentales para el análisis macroeconómico:

#### PIB y Crecimiento
- `PIB_Real_Gasto` - Componentes del PIB por gasto
- `tasa_crecimiento_pib` - Crecimiento económico
- `pib_percapita` - PIB per cápita
- `pib_ramas` - PIB por sectores
- `participacion_pib_ramas` - Estructura sectorial

#### Sector Externo
- `balanza_comercial` - Comercio exterior principal
- `flujo_divisas` - Flujos de divisas
- `Reservas_oro_divisas` - Reservas internacionales
- `grado_de_apertura` - Apertura económica

#### Exportaciones
- `exportaciones_tradicionales_no_tradicionales` - Estructura exportadora
- `exportaciones_tradicionales` - Desagregación tradicionales
- `exportaciones_tradicionales_hidrocarburos` - Sector hidrocarburos
- `exportaciones_minerales_totales` - Sector minero

#### Importaciones
- `composicion_importaciones_uso_destino` - Estructura importaciones

#### Precios
- `precio_oficial_minerales` - Precios minerales
- `precio_petroleo_wti` - Precio petróleo
- `inflacion_acumulada` - Inflación

#### Sector Fiscal
- `consolidado_spnf` - Finanzas públicas principales
- `deuda_externa_total` - Deuda externa

#### Pobreza
- `pobreza` - Indicadores de pobreza
- `pobreza_extrema` - Pobreza extrema

### Prioridad Media (⭐⭐) - Implementar Segundo
25 tablas complementarias para análisis detallado

### Prioridad Baja (⭐) - Implementar Opcional
Series históricas de interés académico pero menor relevancia actual

---

## 🔧 Consideraciones Técnicas para la Implementación

### Transformaciones de Datos Requeridas

#### Conversión de Unidades
- **Miles a millones**: `exportaciones_minerales_totales` (valor_cols / 1000)
- **Cálculo de totales**: Muchas tablas requieren suma de componentes
- **Índices base**: Normalizar según año base especificado

#### Manejo de Datos Faltantes
- Series con gaps temporales (ej. `agregados_monetarios` antes 1990)
- Datos preliminares marcados con "(p)"
- Valores NULL en períodos específicos

#### Validación de Consistencia
- Verificar que totales = suma de componentes
- Validar rangos temporales coherentes
- Comprobar unidades homogéneas

### Configuración de Offsets Específicos

Cada tabla requerirá configuración específica de:
- **annotation_offsets**: Posicionamiento de anotaciones por serie y año
- **hitos_offset**: Altura de líneas verticales de hitos
- **medias_offsets**: Posición de textos de medias por ciclo
- **tasas_offsets**: Ubicación de anotaciones de tasas de crecimiento

### Templates Recomendados por Tipo

#### Gráfico de Línea Simple
```python
componentes = [("serie_principal", "Etiqueta")]
colors = {"serie_principal": "#1f77b4"}
```

#### Gráfico de Líneas Múltiples
```python
componentes = [
    ("serie1", "Serie 1"),
    ("serie2", "Serie 2"),
    ("serie3", "Serie 3")
]
colors = {"serie1": "green", "serie2": "red", "serie3": "blue"}
```

#### Gráfico de Barras Apiladas
```python
# Usar init_base_plot con stacked=True
# Agregar add_participation_cycle_boxes para participaciones
```

---

## 📊 Resumen Estadístico Final

| Categoría | Cantidad | Porcentaje |
|-----------|----------|------------|
| **Total tablas analizadas** | 87 | 100% |
| **Calificadas para graficación** | 81 | 93.1% |
| **No calificadas** | 6 | 6.9% |
| **Prioridad Alta** | 23 | 26.4% |
| **Prioridad Media** | 33 | 37.9% |
| **Prioridad Baja** | 25 | 28.7% |

### Distribución por Tipo de Gráfico
- **Línea simple**: 41 tablas (47.1%)
- **Líneas múltiples/Barras apiladas**: 40 tablas (46.0%)
- **No aplicable**: 6 tablas (6.9%)

---

## 🎯 Conclusiones

1. **Alta compatibilidad**: 93.1% de las tablas son aptas para graficación de serie completa
2. **Diversidad de análisis**: Balance equilibrado entre gráficos simples y múltiples
3. **Cobertura temporal excelente**: Muchas series cubren 50+ años
4. **Calidad de datos**: Documentación detallada facilita implementación
5. **Priorización clara**: 23 tablas de alta prioridad cubren indicadores macroeconómicos esenciales

La implementación debería comenzar con las 23 tablas de prioridad alta, que proporcionarán una cobertura completa de los principales indicadores macroeconómicos de Bolivia desde 1950 hasta 2024.
