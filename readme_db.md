# Tabla: PIB_Real_Gasto

## 📌 Descripción de la Tabla `PIB_Real_Gasto`
Esta tabla almacena el Producto Interno Bruto real desagregado por componentes de gasto para Bolivia, en base a bolivianos constantes de 1990, desde 1950 hasta 2023.

### 📄 Columnas:
| Columna                   | Tipo    | Descripción                                              | Unidad                                  |
|---------------------------|---------|----------------------------------------------------------|-----------------------------------------|
| `año`                     | INTEGER | Año del registro                                         | Año                                     |
| `gastos_consumo`          | REAL    | Consumo total                                            | Miles de bolivianos constantes de 1990  |
| `formacion_capital`       | REAL    | Formación bruta de capital                               | Miles de bolivianos constantes de 1990  |
| `exportacion_bienes_servicios` | REAL    | Exportaciones de bienes y servicios                       | Miles de bolivianos constantes de 1990  |
| `importacion_bienes`      | REAL    | Importaciones de bienes                                   | Miles de bolivianos constantes de 1990  |
| `pib_real_base_1990`      | REAL    | PIB real (base 1990)                                      | Miles de bolivianos constantes de 1990  |
| `consumo_privado`         | REAL    | Consumo privado                                           | Miles de bolivianos constantes de 1990  |
| `consumo_publico`         | REAL    | Consumo público                                           | Miles de bolivianos constantes de 1990  |

## 📌 Período y Unidades
- **Período:** 1950 – 2023  
- **Unidad base:** Miles de bolivianos constantes de 1990  

## 📌 Fuente
- Archivo Excel: `reports/pruebas.xls`  

---

# Tabla: pib_ramas

## 📌 Descripción de la Tabla `pib_ramas`
Desagrega anualmente el PIB por ramas de actividad económica para analizar la contribución sectorial (1950–2022).

### 📄 Columnas:
| Columna                   | Tipo    | Descripción                                                                    | Unidad                                  |
|---------------------------|---------|--------------------------------------------------------------------------------|-----------------------------------------|
| `año`                     | INTEGER | Año del registro                                                               | Año                                     |
| `agropecuario`            | REAL    | Actividad agropecuaria                                                         | Miles de bolivianos constantes de 1990  |
| `minas_canteras_total`    | REAL    | Minería y petróleo (suma de minería + petróleo)                                 | Miles de bolivianos constantes de 1990  |
| `mineria`                 | REAL    | Minería                                                                         | Miles de bolivianos constantes de 1990  |
| `petroleo`                | REAL    | Petróleo                                                                        | Miles de bolivianos constantes de 1990  |
| `industria_manufacturera` | REAL    | Industria manufacturera                                                         | Miles de bolivianos constantes de 1990  |
| `construcciones`          | REAL    | Construcciones                                                                  | Miles de bolivianos constantes de 1990  |
| `energia`                 | REAL    | Producción energética (electricidad, gas y agua)                                | Miles de bolivianos constantes de 1990  |
| `transportes`             | REAL    | Transportes, almacenamiento y comunicaciones                                     | Miles de bolivianos constantes de 1990  |
| `comercio_finanzas`       | REAL    | Comercio y finanzas (rubros 7–8)                                                | Miles de bolivianos constantes de 1990  |
| `gobierno_general`        | REAL    | Gobierno general                                                                 | Miles de bolivianos constantes de 1990  |
| `propiedad_vivienda`      | REAL    | Propiedad de vivienda                                                            | Miles de bolivianos constantes de 1990  |
| `servicios`               | REAL    | Servicios (comunales, sociales, personales, hoteles)                             | Miles de bolivianos constantes de 1990  |
| `derechos_imp`            | REAL    | Derechos de importación / Impuestos                                              | Miles de bolivianos constantes de 1990  |
| `pib_nominal`             | REAL    | Producto Interno Bruto nominal                                                   | Miles de bolivianos constantes de 1990  |
| `pib_real`                | REAL    | Producto Interno Bruto real                                                      | Miles de bolivianos constantes de 1990  |

## 📌 Período y Unidades
- **Período:** 1950 – 2022  
- **Unidad base:** Miles de bolivianos constantes de 1990  

## 📌 Fuente
- Archivo Excel: `db/pruebas.xlsx`  

---

# Tabla: Participacion_PIB

## 📌 Descripción de la Tabla `Participacion_PIB`
Almacena la participación de exportaciones e importaciones como porcentaje del PIB anual para medir su peso relativo en la actividad económica (1950–2023).

### 📄 Columnas:
| Columna               | Tipo   | Descripción                          | Unidad    |
|-----------------------|--------|--------------------------------------|-----------|
| `año`                 | INTEGER| Año del registro                     | Año       |
| `exportaciones_pib`   | REAL   | Exportaciones como % del PIB         | Porcentaje|
| `importaciones_pib`   | REAL   | Importaciones como % del PIB         | Porcentaje|

## 📌 Período y Unidades
- **Período:** 1950 – 2023  
- **Unidad base:** Porcentaje  

## 📌 Fuente
- Archivo Excel: `reports/pruebas.xls`  

---

# Tabla: tasa_crecimiento_pib

## 📌 Descripción de la Tabla `tasa_crecimiento_pib`
Registra la variación porcentual anual del PIB para evaluar el ritmo de crecimiento económico (1951–2024).

### 📄 Columnas:
| Columna      | Tipo    | Descripción                                            | Unidad    |
|--------------|---------|--------------------------------------------------------|-----------|
| `año`        | INTEGER | Año del registro                                       | Año       |
| `crecimiento`| REAL    | Tasa de crecimiento anual del PIB (%)                  | Porcentaje|

## 📌 Período y Unidades
- **Período:** 1951 – 2024  
- **Unidad base:** Porcentaje  

## 📌 Fuente
- Archivo Excel: `db/pruebas.xlsx`  

---

# Tabla: participacion_x_m_pib

## 📌 Descripción de la Tabla `participacion_x_m_pib`
Muestra la participación de exportaciones (X) e importaciones (M) como porcentaje del PIB, para medir su incidencia en la actividad económica (1950–2023).

### 📄 Columnas:
| Columna  | Tipo    | Descripción                  | Unidad    |
|----------|---------|------------------------------|-----------|
| `año`    | INTEGER | Año del registro             | Año       |
| `x`      | REAL    | Exportaciones como % del PIB | Porcentaje|
| `m`      | REAL    | Importaciones como % del PIB | Porcentaje|

## 📌 Período y Unidades
- **Período:** 1950 – 2023  
- **Unidad base:** Porcentaje  

## 📌 Fuente
- Archivo Excel: `db/pruebas.xlsx`  

---

# Tabla: participacion_pib_ramas

## 📌 Descripción de la Tabla `participacion_pib_ramas`
Almacena el porcentaje anual que representa cada rama de actividad económica sobre el PIB total. Incluye agregados calculados automáticamente (minas_canteras_total, comercio_finanzas) (1950–2023).

### 📄 Columnas:
| Columna                   | Tipo    | Descripción                                                         | Unidad    |
|---------------------------|---------|---------------------------------------------------------------------|-----------|
| `año`                     | INTEGER | Año del registro                                                    | Año       |
| `agropecuario`            | REAL    | Agricultura, silvicultura, caza y pesca (% PIB)                    | Porcentaje|
| `minas_canteras_total`    | REAL    | Minería + Petróleo (% PIB)                                          | Porcentaje|
| `mineria`                 | REAL    | Minerales metálicos y no metálicos (% PIB)                          | Porcentaje|
| `petroleo`                | REAL    | Petróleo crudo y gas natural (% PIB)                                | Porcentaje|
| `industria_manufacturera` | REAL    | Industria manufacturera (% PIB)                                      | Porcentaje|
| `construcciones`          | REAL    | Construcción (% PIB)                                                 | Porcentaje|
| `energia`                 | REAL    | Electricidad, gas y agua (% PIB)                                     | Porcentaje|
| `transportes`             | REAL    | Transporte, almacenamiento y comunicaciones (% PIB)                  | Porcentaje|
| `comercio_finanzas`       | REAL    | Comercio y servicios financieros/empresas (% PIB)                    | Porcentaje|
| `gobierno_general`        | REAL    | Gobierno general (% PIB)                                             | Porcentaje|
| `propiedad_vivienda`      | REAL    | Propiedad de vivienda (% PIB)                                        | Porcentaje|
| `servicios`               | REAL    | Servicios comunales, sociales, personales y hoteles (% PIB)         | Porcentaje|

## 📌 Período y Unidades
- **Período:** 1950 – 2023  
- **Unidad base:** Porcentaje  

## 📌 Fuente
- Base SQLite “participacion.db” creado a partir de archivos Excel.  
- Cálculos de agregados:  
  - `minas_canteras_total = mineria + petroleo`  
  - `comercio_finanzas = comercio + servicios_financieros + servicios_a_empresas + restaurantes_y_hoteles`  

---

# Tabla: balanza_comercial

## 📌 Descripción de la Tabla `balanza_comercial`
Registra anualmente el valor de exportaciones, importaciones y saldo comercial de Bolivia (1949–2024).

### 📄 Columnas:
| Columna           | Tipo    | Descripción                                       | Unidad            |
|-------------------|---------|---------------------------------------------------|-------------------|
| `año`             | INTEGER | Año del registro                                  | Año               |
| `exportaciones`   | REAL    | Valor de exportaciones                            | Millones USD      |
| `importaciones`   | REAL    | Valor de importaciones                            | Millones USD      |
| `saldo_comercial` | REAL    | Exportaciones − Importaciones                     | Millones USD      |

## 📌 Período y Unidades
- **Período:** 1949 – 2024  
- **Unidad base:** Millones de dólares (USD)  

## 📌 Fuente
- INE: Memorias del Banco Central de Bolivia  
- URL: https://nube.ine.gob.bo/index.php/s/nMPCP2wBQqnx7c1/download  

---

# Tabla: flujo_divisas

## 📌 Descripción de la Tabla `flujo_divisas`
Registra anualmente los ingresos, egresos y flujo neto de divisas en Bolivia, para evaluar la balanza de transacciones internacionales (1985–2023).

### 📄 Columnas:
| Columna             | Tipo    | Descripción                                | Unidad         |
|---------------------|---------|--------------------------------------------|----------------|
| `año`               | INTEGER | Año del registro                           | Año            |
| `ingreso_divisas`   | REAL    | Ingresos de divisas                        | Millones USD   |
| `egreso_divisas`    | REAL    | Egresos de divisas                         | Millones USD   |
| `flujo_neto_divisas`| REAL    | Ingresos − Egresos                         | Millones USD   |

## 📌 Período y Unidades
- **Período:** 1985 – 2023  
- **Unidad base:** Millones de dólares (USD)  

## 📌 Fuente
- UDAPE: “Balanza cambiaria”  
- URL: https://dossier.udape.gob.bo/res/balanza%20cambiaria  

---

# Tabla: grado_de_apertura

## 📌 Descripción de la Tabla `grado_de_apertura`
Mide la apertura económica como la suma de exportaciones e importaciones en relación al PIB anual (1950–2022).

### 📄 Columnas:
| Columna | Tipo    | Descripción                                     | Unidad    |
|---------|---------|-------------------------------------------------|-----------|
| `año`   | INTEGER | Año del registro                                | Año       |
| `grado` | REAL    | (Exportaciones + Importaciones) / PIB (%)       | Porcentaje|

## 📌 Período y Unidades
- **Período:** 1950 – 2022  
- **Unidad base:** Porcentaje  

## 📌 Fuente
- Archivo Excel: `db/pruebas.xlsx`  

---

# Tabla: Reservas_oro_divisas

## 📌 Descripción de la Tabla `Reservas_oro_divisas`
Registra anualmente el volumen de reservas internacionales en oro y divisas, en millones de dólares (1950–2023).

### 📄 Columnas:
| Columna            | Tipo    | Descripción                              | Unidad         |
|--------------------|---------|------------------------------------------|----------------|
| `año`              | INTEGER | Año del registro                         | Año            |
| `reservas_totales` | REAL    | Reservas totales en oro y divisas        | Millones USD   |

## 📌 Período y Unidades
- **Período:** 1950 – 2023  
- **Unidad base:** Millones de dólares (USD)  

## 📌 Fuente
- Banco Mundial (1960–2023) / BCB (1950–1960)  
- URL: https://datos.bancomundial.org/indicador/FI.RES.TOTL.CD?locations=BO  

---

# Tabla: exportaciones_totales

## 📌 Descripción de la Tabla `exportaciones_totales`
Registra el valor anual de exportaciones, desglosadas en productos tradicionales y no tradicionales, junto con su valor total (1980–2023).

### 📄 Columnas:
| Columna                      | Tipo    | Descripción                                | Unidad         |
|------------------------------|---------|--------------------------------------------|----------------|
| `año`                        | INTEGER | Año del registro                           | Año            |
| `productos_tradicionales`    | REAL    | Valor de exportaciones tradicionales       | Millones USD   |
| `productos_no_tradicionales` | REAL    | Valor de exportaciones no tradicionales    | Millones USD   |
| `total_valor_oficial`        | REAL    | Suma oficial de todas las exportaciones    | Millones USD   |

## 📌 Período y Unidades
- **Período:** 1980 – 2023  
- **Unidad base:** Millones de dólares (USD)  

## 📌 Fuente
- INE: https://nube.ine.gob.bo/index.php/s/zUQc65wIGkw1KUy/download  

---

# Tabla: exportaciones_minerales_totales

## 📌 Descripción de la Tabla `exportaciones_minerales_totales`
Registra anualmente el volumen (en kilos finos) y el valor (en miles de dólares) de las exportaciones de minerales para evaluar la evolución del sector minero (1952–2023).

### 📄 Columnas:
| Columna          | Tipo    | Descripción                                | Unidad                  |
|------------------|---------|--------------------------------------------|-------------------------|
| `año`            | INTEGER | Año del registro                           | Año                     |
| `estaño_volumen` | REAL    | Volumen de estaño                           | Kilos finos             |
| `estaño_valor`   | REAL    | Valor de estaño                             | Miles USD               |
| `plomo_volumen`  | REAL    | Volumen de plomo                            | Kilos finos             |
| `plomo_valor`    | REAL    | Valor de plomo                              | Miles USD               |
| `zinc_volumen`   | REAL    | Volumen de zinc                             | Kilos finos             |
| `zinc_valor`     | REAL    | Valor de zinc                               | Miles USD               |
| `plata_volumen`  | REAL    | Volumen de plata                            | Kilos finos             |
| `plata_valor`    | REAL    | Valor de plata                              | Miles USD               |
| `wolfram_volumen`| REAL    | Volumen de wólfram                          | Kilos finos             |
| `wolfram_valor`  | REAL    | Valor de wólfram                            | Miles USD               |
| `cobre_volumen`  | REAL    | Volumen de cobre                            | Kilos finos             |
| `cobre_valor`    | REAL    | Valor de cobre                              | Miles USD               |
| `antimonio_volumen` | REAL    | Volumen de antimonio                       | Kilos finos             |
| `antimonio_valor`   | REAL    | Valor de antimonio                         | Miles USD               |
| `oro_volumen`    | REAL    | Volumen de oro                              | Kilos finos             |
| `oro_valor`      | REAL    | Valor de oro                                | Miles USD               |

## 📌 Período y Unidades
- **Período:** 1952 – 2023  
- **Unidades:**  
  - Volumen en kilos finos  
  - Valor en miles de dólares (USD)  

## 📌 Fuente
- 1952–1987: Informes del Banco Central de Bolivia  
- 1987–2023: UDAPE (https://dossier.udape.gob.bo/res/VOLUMEN%20Y%20VALOR%20DE%20EXPORTACIONES%20DE%20MINERALES)  

---

# Tabla: exportaciones_tradicionales

## 📌 Descripción de la Tabla `exportaciones_tradicionales`
Registra el valor anual de exportaciones tradicionales desglosadas en minerales e hidrocarburos (1992–2024).

### 📄 Columnas:
| Columna    | Tipo    | Descripción                                      | Unidad         |
|------------|---------|--------------------------------------------------|----------------|
| `año`      | INTEGER | Año del registro                                 | Año            |
| `minerales`| REAL    | Valor de exportaciones de minerales              | Millones USD   |
| `hidrocarburos` | REAL | Valor de exportaciones de hidrocarburos        | Millones USD   |

## 📌 Período y Unidades
- **Período:** 1992 – 2024  
- **Unidad base:** Millones de dólares (USD)  

## 📌 Fuente
- INE: https://www.ine.gob.bo/index.php/estadisticas-economicas/comercio-exterior/cuadros-estadisticos-exportaciones/  

---

# Tabla: exportaciones_tradicionales_no_tradicionales

## 📌 Descripción de la Tabla `exportaciones_tradicionales_no_tradicionales`
Desglosa anualmente las exportaciones en tradicionales y no tradicionales, para analizar su evolución y peso relativo (1980–2024).

### 📄 Columnas:
| Columna         | Tipo    | Descripción                                   | Unidad         |
|-----------------|---------|-----------------------------------------------|----------------|
| `año`           | INTEGER | Año del registro                              | Año            |
| `tradicionales` | REAL    | Exportaciones tradicionales                   | Millones USD   |
| `no_tradicionales` | REAL | Exportaciones no tradicionales               | Millones USD   |

## 📌 Período y Unidades
- **Período:** 1980 – 2024  
- **Unidad base:** Millones de dólares (USD)  

## 📌 Fuente
- INE: https://www.ine.gob.bo/index.php/estadisticas-economicas/comercio-exterior/cuadros-estadisticos-exportaciones/  

---

# Tabla: participacion_exp_trad_no_trad

## 📌 Descripción de la Tabla `participacion_exp_trad_no_trad`
Almacena la participación porcentual de exportaciones tradicionales y no tradicionales para medir su peso en el total de exportaciones (1980–2023).

### 📄 Columnas:
| Columna       | Tipo    | Descripción                                    | Unidad    |
|---------------|---------|------------------------------------------------|-----------|
| `año`         | INTEGER | Año del registro                               | Año       |
| `exp_trad`    | REAL    | Exportaciones tradicionales (% del total)      | Porcentaje|
| `exp_no_trad` | REAL    | Exportaciones no tradicionales (% del total)   | Porcentaje|

## 📌 Período y Unidades
- **Período:** 1980 – 2023  
- **Unidad base:** Porcentaje  

## 📌 Fuente
- Archivo Excel: `db/pruebas.xlsx`  

---

# Tabla: exportaciones_tradicionales_hidrocarburos

## 📌 Descripción de la Tabla `exportaciones_tradicionales_hidrocarburos`
Registra anualmente el valor de exportaciones de hidrocarburos, desglosando gas natural y otros hidrocarburos (1992–2024).

### 📄 Columnas:
| Columna          | Tipo    | Descripción                                   | Unidad         |
|------------------|---------|-----------------------------------------------|----------------|
| `año`            | INTEGER | Año del registro                              | Año            |
| `hidrocarburos`  | REAL    | Total de exportaciones de hidrocarburos       | Millones USD   |
| `gas_natural`    | REAL    | Exportaciones de gas natural                  | Millones USD   |
| `otros_hidrocarburos`| REAL| Exportaciones de otros hidrocarburos          | Millones USD   |

## 📌 Período y Unidades
- **Período:** 1992 – 2024  
- **Unidad base:** Millones de dólares (USD)  

## 📌 Fuente
- INE: https://www.ine.gob.bo/index.php/estadisticas-economicas/comercio-exterior/cuadros-estadisticos-exportaciones/  

---

# Tabla: exportacion_gas_natural

## 📌 Descripción de la Tabla `exportacion_gas_natural`
Registra el volumen, precio y valor anual de las exportaciones de gas natural, para analizar su evolución en el período 1987–2023.

### 📄 Columnas:
| Columna         | Tipo  | Descripción                                                     | Unidad                        |
|-----------------|-------|-----------------------------------------------------------------|-------------------------------|
| `año`           | INTEGER | Año del registro                                              | Año                           |
| `volumen_MMMc`  | REAL  | Volumen en millones de metros cúbicos (MMmc)                   | Millones m³                   |
| `volumen_MMPC`  | REAL  | Volumen en millones de pies cúbicos (MMPC)                     | Millones pies³                |
| `precio_usd_MPC`| REAL  | Precio en USD por mil pies cúbicos (USD/MPC)                   | USD por mil pies cúbicos      |
| `valor`         | REAL  | Valor de las exportaciones de gas natural                       | Miles USD                     |

## 📌 Período y Unidades
- **Período:** 1987 – 2023  
- **Unidades:**  
  - Volumen: Millones m³ y millones pies³  
  - Precio: USD/MPC  
  - Valor: Miles USD  

## 📌 Fuente
- UDAPE: https://dossier.udape.gob.bo/res/EXPORTACIÓN%20DE%20GAS%20NATURAL  

---

# Tabla: exportacion_gas_natural_contratos

## 📌 Descripción de la Tabla `exportacion_gas_natural_contratos`
Detalla las exportaciones de gas natural por contrato y destino (Argentina o Brasil) para el período 1992–2023.

### 📄 Columnas:
| Columna   | Tipo    | Descripción                                                 | Unidad         |
|-----------|---------|-------------------------------------------------------------|----------------|
| `año`     | INTEGER | Año del registro                                            | Año            |
| `contrato`| TEXT    | Nombre del contrato de exportación                          | Texto          |
| `destino` | TEXT    | Destino del gas (Argentina o Brasil)                        | Texto          |
| `monto`   | REAL    | Valor de exportación por contrato                           | Millones USD   |

## 📌 Período y Unidades
- **Período:** 1992 – 2023  
- **Unidad base:** Millones de dólares (USD)  

## 📌 Fuente
- UDAPE: https://dossier.udape.gob.bo/res/VALOR%20DE%20EXPORTACIÓN%20DE%20GAS%20NATURAL%20POR%20CONTRATO  

---

# Tabla: participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos

## 📌 Descripción de la Tabla `participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos`
Almacena la participación porcentual del gas natural y otros hidrocarburos en el total exportado de hidrocarburos (1980–2023).

### 📄 Columnas:
| Columna             | Tipo    | Descripción                                                      | Unidad    |
|---------------------|---------|------------------------------------------------------------------|-----------|
| `año`               | INTEGER | Año del registro                                                 | Año       |
| `exportacion_gas`   | REAL    | Gas natural como % del total de hidrocarburos                    | Porcentaje|
| `otros_hidrocarburos`| REAL   | Otros hidrocarburos como % del total de hidrocarburos            | Porcentaje|

## 📌 Período y Unidades
- **Período:** 1980 – 2023  
- **Unidad base:** Porcentaje  

## 📌 Fuente
- Archivo Excel: `db/pruebas.xlsx`  

---

# Tabla: participacion_hidrocarburos_minerales_exportaciones_tradicionales

## 📌 Descripción de la Tabla `participacion_hidrocarburos_minerales_exportaciones_tradicionales`
Registra la participación porcentual de hidrocarburos y minerales en las exportaciones tradicionales (1980–2023).

### 📄 Columnas:
| Columna      | Tipo    | Descripción                                                    | Unidad    |
|--------------|---------|----------------------------------------------------------------|-----------|
| `año`        | INTEGER | Año del registro                                               | Año       |
| `minerales`  | REAL    | Minerales como % del total de exportaciones tradicionales      | Porcentaje|
| `hidrocarburos`| REAL  | Hidrocarburos como % del total de exportaciones tradicionales  | Porcentaje|

## 📌 Período y Unidades
- **Período:** 1980 – 2023  
- **Unidad base:** Porcentaje  

## 📌 Fuente
- Archivo Excel: `db/pruebas.xlsx`  

---

# Tabla: composicion_importaciones_uso_destino

## 📌 Descripción de la Tabla `composicion_importaciones_uso_destino`
Clasifica el valor anual de las importaciones según uso económico: bienes de consumo, materias primas/productos intermedios, bienes de capital y otros usos. Datos expresados en CIF frontera (1980–2024).

### 📄 Columnas:
| Columna                             | Tipo    | Descripción                                         | Unidad         |
|-------------------------------------|---------|-----------------------------------------------------|----------------|
| `año`                               | INTEGER | Año del registro                                    | Año            |
| `bienes_consumo`                    | REAL    | Bienes de consumo                                   | Millones USD (CIF) |
| `materias_primas_productos_intermedios` | REAL    | Materias primas / productos intermedios             | Millones USD (CIF) |
| `bienes_capital`                    | REAL    | Bienes de capital                                   | Millones USD (CIF) |
| `diversos`                          | REAL    | Otros usos                                          | Millones USD (CIF) |
| `total_valor_oficial_cif`           | REAL    | Total valor oficial CIF                             | Millones USD (CIF) |

## 📌 Período y Unidades
- **Período:** 1980 – 2024  
- **Unidad base:** Millones de dólares (CIF)  

## 📌 Fuente
- INE: https://www.ine.gob.bo/index.php/estadisticas-economicas/comercio-exterior/importaciones-cuadros-estadisticos/  

---

# Tabla: participacion_composicion_importaciones_uso_destino

## 📌 Descripción de la Tabla `participacion_composicion_importaciones_uso_destino`
Almacena la participación porcentual de cada categoría de importaciones sobre el total CIF frontera (1980–2024).

### 📄 Columnas:
| Columna                             | Tipo    | Descripción                                         | Unidad    |
|-------------------------------------|---------|-----------------------------------------------------|-----------|
| `año`                               | INTEGER | Año del registro                                    | Año       |
| `bienes_consumo`                    | REAL    | Bienes de consumo (% del total CIF)                 | Porcentaje|
| `materias_primas_productos_intermedios` | REAL    | Materias primas/productos intermedios (% del total) | Porcentaje|
| `bienes_capital`                    | REAL    | Bienes de capital (% del total CIF)                 | Porcentaje|
| `diversos`                          | REAL    | Otros usos (% del total CIF)                        | Porcentaje|
| `total_cif`                         | REAL    | Total importaciones CIF (siempre 100%)               | Porcentaje|

## 📌 Período y Unidades
- **Período:** 1980 – 2024  
- **Unidad base:** Porcentaje  

## 📌 Fuente
- Archivo Excel: `db/pruebas.xlsx`  

---

# Tabla: tu

## 📌 Descripción de la Tabla `tu`
Registra exportaciones no tradicionales desglosadas por producto (1992–2024).

### 📄 Columnas:
| Columna            | Tipo    | Descripción                                | Unidad         |
|--------------------|---------|--------------------------------------------|----------------|
| `año`              | INTEGER | Año del registro                           | Año            |
| `total`            | REAL    | Total exportaciones no tradicionales        | Millones USD   |
| `castaña`          | REAL    | Exportaciones de castaña                   | Millones USD   |
| `café`             | REAL    | Exportaciones de café                      | Millones USD   |
| `cacao`            | REAL    | Exportaciones de cacao                     | Millones USD   |
| `azúcar`           | REAL    | Exportaciones de azúcar                    | Millones USD   |
| `bebidas`          | REAL    | Exportaciones de bebidas                   | Millones USD   |
| `gomas`            | REAL    | Exportaciones de gomas                      | Millones USD   |
| `cueros`           | REAL    | Exportaciones de cueros                     | Millones USD   |
| `maderas`          | REAL    | Exportaciones de maderas                    | Millones USD   |
| `algodón`          | REAL    | Exportaciones de algodón                    | Millones USD   |
| `soya`             | REAL    | Exportaciones de soya                       | Millones USD   |
| `joyería`          | REAL    | Exportaciones de joyería                    | Millones USD   |
| `joyería_con_oro_imp` | REAL | Exportaciones de joyería con oro importado | Millones USD   |
| `otros`            | REAL    | Exportaciones de otros productos            | Millones USD   |

## 📌 Período y Unidades
- **Período:** 1992 – 2024  
- **Unidad base:** Millones de dólares (USD)  

## 📌 Fuente
- INE: https://www.ine.gob.bo/index.php/estadisticas-economicas/comercio-exterior/cuadros-estadisticos-exportaciones/  

---

# Tabla: precio_minerales

## 📌 Descripción de la Tabla `precio_minerales`
Registra el precio anual de minerales principales expresado en USD según la unidad de medida específica (1980–2015).

### 📄 Columnas:
| Columna    | Tipo      | Descripción                                               | Unidad                        |
|------------|-----------|-----------------------------------------------------------|-------------------------------|
| `año`      | INTEGER   | Año del registro                                          | Año                           |
| `Zinc`     | REAL      | Precio del Zinc (Libras Finas – L.F)                      | USD (L.F.)                    |
| `Estaño`   | REAL      | Precio del Estaño (Libras Finas – L.F)                    | USD (L.F.)                    |
| `Oro`      | REAL      | Precio del Oro (Onzas Troy – O.T.)                        | USD (O.T.)                    |
| `Plata`    | REAL      | Precio de la Plata (Onzas Troy – O.T.)                    | USD (O.T.)                    |
| `Antimonio`| REAL      | Precio del Antimonio (Toneladas Métricas Finas – T.M.F.)  | USD (T.M.F.)                  |
| `Plomo`    | REAL      | Precio del Plomo (Libras Finas – L.F)                     | USD (L.F.)                    |
| `Wólfram`  | REAL      | Precio del Wólfram (Libras Finas – L.F)                    | USD (L.F.)                    |
| `Cobre`    | REAL      | Precio del Cobre (Libras Finas – L.F)                     | USD (L.F.)                    |

### 🛠 Unidades de Medida  
- **L.F. (Libras Finas)** → Zinc, Estaño, Plomo, Cobre  
- **O.T. (Onzas Troy)** → Oro, Plata  
- **T.M.F. (Toneladas Métricas Finas)** → Antimonio  

## ⚠️ Notas  
- **Frecuencia:** Datos anuales desde 1980 hasta 2015.  
- **Fuente:** Ministerio de Minería y Metalurgia: https://mineria.gob.bo/revista/pdf/20170817-10-15-28.pdf  

---

# Tabla: precio_oficial_minerales

## 📌 Descripción de la Tabla `precio_oficial_minerales`
Registra el precio oficial anual de minerales principales en USD (1950–2024).

### 📄 Columnas:
| Columna   | Tipo  | Descripción                                | Unidad  |
|-----------|-------|--------------------------------------------|---------|
| `año`     | INTEGER | Año del registro                         | Año     |
| `zinc`    | REAL  | Precio oficial del Zinc en USD            | USD     |
| `estaño`  | REAL  | Precio oficial del Estaño en USD          | USD     |
| `oro`     | REAL  | Precio oficial del Oro en USD             | USD     |
| `plata`   | REAL  | Precio oficial de la Plata en USD         | USD     |
| `antimonio` | REAL | Precio oficial del Antimonio en USD       | USD     |
| `plomo`   | REAL  | Precio oficial del Plomo en USD           | USD     |
| `wolfram` | REAL  | Precio oficial del Wólfram en USD         | USD     |
| `cobre`   | REAL  | Precio oficial del Cobre en USD           | USD     |
| `bismuto` | REAL  | Precio oficial del Bismuto en USD         | USD     |
| `cadmio`  | REAL  | Precio oficial del Cadmio en USD          | USD     |
| `manganeso` | REAL | Precio oficial del Manganeso en USD       | USD     |

## 📌 Período y Unidades
- **Período:** 1950 – 2024  
- **Unidad base:** Dólares Americanos (USD)  

## 📌 Fuente
- 1950–1980: Informes del Banco Central de Bolivia  
- 1980–2015: Ministerio de Minería y Metalurgia  
- 2015–2024: Ministerio de Minería y Metalurgia (Dossier 1980–2023)

---

# Tabla: precio_petroleo_wti

## 📌 Descripción de la Tabla `precio_petroleo_wti`
Registra el precio anual del petróleo WTI en USD por barril (1996–2023).

### 📄 Columnas:
| Columna  | Tipo   | Descripción                  | Unidad     |
|----------|--------|------------------------------|------------|
| `año`    | INTEGER| Año del registro             | Año        |
| `precio` | REAL   | Precio del petróleo WTI      | USD/barril |

## 📌 Período y Unidades
- **Período:** 1996 – 2023  
- **Unidad base:** Dólares Americanos (USD)  

## 📌 Fuente
- UDAPE: https://dossier.udape.gob.bo/res/PRECIO%20INTERNACIONAL%20DEL%20PETR%C3%93LEO%20(WTI)

---

# Tabla: produccion_minerales

## 📌 Descripción de la Tabla `produccion_minerales`
Almacena la producción anual de minerales principales en toneladas finas para el período 1985–2021.

### 📄 Columnas:
| Columna    | Tipo    | Descripción                              | Unidad            |
|------------|---------|------------------------------------------|-------------------|
| `año`      | INTEGER | Año de la producción minera              | Año               |
| `zinc`     | REAL    | Producción de Zinc                       | Toneladas finas   |
| `estaño`   | REAL    | Producción de Estaño                     | Toneladas finas   |
| `oro`      | REAL    | Producción de Oro                        | Toneladas finas   |
| `plata`    | REAL    | Producción de Plata                      | Toneladas finas   |
| `antimonio`| REAL    | Producción de Antimonio                  | Toneladas finas   |
| `plomo`    | REAL    | Producción de Plomo                      | Toneladas finas   |
| `wolfram`  | REAL    | Producción de Wólfram                    | Toneladas finas   |
| `cobre`    | REAL    | Producción de Cobre                      | Toneladas finas   |

## 📌 Período y Unidades
- **Período:** 1985 – 2021  
- **Unidad base:** Toneladas finas  

## 📌 Fuente
- Ministerio de Minería y Metalurgia: https://mineria.gob.bo/revista/pdf/20170817-10-15-28.pdf  

---

# Tabla: consolidado_spnf

## 📌 Descripción de la Tabla `consolidado_spnf`
Registra las operaciones consolidadas del Sector Público No Financiero (SPNF): ingresos, egresos, superávit/deficit global y primario, y financiamiento, para el período 1990–2023.

### 📄 Columnas:
| Columna             | Tipo    | Descripción                                            | Unidad             |
|---------------------|---------|--------------------------------------------------------|--------------------|
| `año`               | INTEGER | Año del registro                                       | Año                |
| `ingresos_totales`  | REAL    | Ingresos totales del SPNF                              | Millones BOB       |
| `egresos_totales`   | REAL    | Egresos totales del SPNF                               | Millones BOB       |
| `sup_o_def_global`  | REAL    | Superávit o déficit global                             | Millones BOB       |
| `financiamiento`    | REAL    | Financiamiento neto                                    | Millones BOB       |
| `sup_o_def_primario`| REAL    | Superávit o déficit primario                           | Millones BOB       |

## 📌 Período y Unidades
- **Período:** 1990 – 2023  
- **Unidad base:** Millones de bolivianos (BOB)  

## 📌 Fuente
- UDAPE: https://dossier.udape.gob.bo/res/operaciones%20consolidadas%20del%20sector  

---

# Tabla: operaciones_empresas_publicas

## 📌 Descripción de la Tabla `operaciones_empresas_publicas`
Registra los ingresos, egresos y resultado fiscal global de empresas públicas como porcentaje del PIB (1990–2020).

### 📄 Columnas:
| Columna            | Tipo    | Descripción                                        | Unidad    |
|--------------------|---------|----------------------------------------------------|-----------|
| `año`              | INTEGER | Año del registro                                   | Año       |
| `ingresos_totales` | REAL    | Ingresos totales de empresas públicas (% PIB)      | Porcentaje|
| `egresos_totales`  | REAL    | Egresos totales de empresas públicas (% PIB)       | Porcentaje|
| `resultado_fiscal_global` | REAL | Resultado fiscal global (% PIB)                | Porcentaje|

## 📌 Período y Unidades
- **Período:** 1990 – 2020  
- **Unidad base:** Porcentaje del PIB  

## 📌 Fuente
- Excel interno (pendiente de fuente exacta en USB)  

---

# Tabla: inversion_publica_total

## 📌 Descripción de la Tabla `inversion_publica_total`
Registra el monto anual de la inversión pública total en Bolivia, en miles de dólares (1990–2023).

### 📄 Columnas:
| Columna | Tipo    | Descripción                            | Unidad        |
|---------|---------|----------------------------------------|---------------|
| `año`   | INTEGER | Año del registro                       | Año           |
| `valor` | REAL    | Inversión pública total                | Miles USD     |

## 📌 Período y Unidades
- **Período:** 1990 – 2023  
- **Unidad base:** Miles de dólares (USD)  

## 📌 Fuente
- UDAPE: https://dossier.udape.gob.bo/res/INVERSIÓN%20PÚBLICA%20POR%20SECTORES  

---

# Tabla: inversion_publica_por_sectores

## 📌 Descripción de la Tabla `inversion_publica_por_sectores`
Distribuye el monto anual de inversión pública entre sectores: extractivo, apoyo a la producción, infraestructura y sector social (1990–2014).

### 📄 Columnas:
| Columna                         | Tipo    | Descripción                                  | Unidad        |
|---------------------------------|---------|----------------------------------------------|---------------|
| `año`                           | INTEGER | Año del registro                             | Año           |
| `extractivo`                    | REAL    | Inversión en sector extractivo               | Miles USD     |
| `apoyo_a_la_produccion`         | REAL    | Inversión en apoyo a la producción           | Miles USD     |
| `infraestructura`               | REAL    | Inversión en infraestructura                  | Miles USD     |
| `sociales`                      | REAL    | Inversión en sector social                    | Miles USD     |
| `total`                         | REAL    | Inversión pública total                       | Miles USD     |

## 📌 Período y Unidades
- **Período:** 1990 – 2014  
- **Unidad base:** Miles de dólares (USD)  

## 📌 Fuente
- UDAPE: https://dossier.udape.gob.bo/res/INVERSIÓN%20PÚBLICA%20POR%20SECTORES  

---

# Tabla: deuda_externa_total

## 📌 Descripción de la Tabla `deuda_externa_total`
Registra el monto anual de la deuda externa total de Bolivia en millones de dólares (1951–2020).

### 📄 Columnas:
| Columna   | Tipo    | Descripción                         | Unidad         |
|-----------|---------|-------------------------------------|----------------|
| `año`     | INTEGER | Año del registro                    | Año            |
| `deuda`   | REAL    | Monto de deuda externa total        | Millones USD   |

## 📌 Período y Unidades
- **Período:** 1951 – 2020  
- **Unidad base:** Millones de dólares (USD)  

## 📌 Fuente
- 1951–1996: Informes del Banco Central de Bolivia  
- 1996–2020: UDAPE (https://dossier.udape.gob.bo/res/DEUDA%20PÚBLICA%20EXTERNA%20DE%20MEDIANO)  

---

# Tabla: deuda_interna

## 📌 Descripción de la Tabla `deuda_interna`
Registra el valor anual del stock de deuda interna manejada por el Tesoro General de la Nación (1993–2022).

### 📄 Columnas:
| Columna | Tipo    | Descripción                         | Unidad         |
|---------|---------|-------------------------------------|----------------|
| `año`   | INTEGER | Año del registro (PK)               | Año            |
| `valor` | REAL    | Stock de deuda interna              | Millones USD   |

## 📌 Período y Unidades
- **Período:** 1993 – 2022  
- **Unidad base:** Millones de dólares (USD)  

## 📌 Fuente
- UDAPE: https://dossier.udape.gob.bo/res/STOCK%20DE%20LA%20DEUDA%20PÚBLICA%20INTERNA%20DEL%20TESORO%20GENERAL%20DE%20LA%20NACIÓN  

---

> **Fin del documento**  
