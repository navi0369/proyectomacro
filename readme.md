# tabla: Producción de Minerales (Toneladas Finas)

## 📌 Descripción de la Tabla `produccion_minerales`
Esta tabla almacena la producción anual de minerales en toneladas finas desde 1985 hasta 2021.

### 📄 Columnas:
| Columna    | Descripción                              | Unidad            |
|------------|------------------------------------------|------------------|
| `año`      | Año de la producción minera             | Año              |
| `Zinc`     | Producción de zinc                      | Toneladas finas  |
| `Estaño`   | Producción de estaño                    | Toneladas finas  |
| `Oro`      | Producción de oro                       | Toneladas finas  |
| `Plata`    | Producción de plata                     | Toneladas finas  |
| `Antimonio`| Producción de antimonio                 | Toneladas finas  |
| `Plomo`    | Producción de plomo                     | Toneladas finas  |
| `Wólfram`  | Producción de wólfram                   | Toneladas finas  |
| `Cobre`    | Producción de cobre                     | Toneladas finas  |

## 📌 Notas:
- **Fuente:** Datos obtenidos del Ministerio de Minería de Bolivia.
    https://mineria.gob.bo/revista/pdf/20170817-10-15-28.pdf
- **Frecuencia:** Datos anuales desde **1985 hasta 2021**.
- **Formato:** Los valores están en **toneladas finas**.


# Tabla: precio_minerales y precio_oficial_minerales
# importante PRECIOS DE MINERALES - REALES (En Dólares Americanos de 1990)

La tabla precio_minerales almacena los precios de distintos minerales en diferentes años. Cada registro representa el precio de un mineral en un año específico.

📊 Estructura de la Tabla
| Columna    | Tipo de Dato | Descripción |
|------------|-------------|-------------|
| año       | INTEGER (PK) | Año del registro |
| Zinc       | REAL        | Precio del Zinc (Libras Finas - L.F) en USD |
| Estaño     | REAL        | Precio del Estaño (Libras Finas - L.F) en USD |
| Oro        | REAL        | Precio del Oro (Onzas Troy - O.T.) en USD |
| Plata      | REAL        | Precio de la Plata (Onzas Troy - O.T.) en USD |
| Antimonio  | REAL        | Precio del Antimonio (Toneladas Métricas Finas - T.M.F.) en USD |
| Plomo      | REAL        | Precio del Plomo (Libras Finas - L.F) en USD |
| Wólfram    | REAL        | Precio del Wólfram (Unidades Libras Finas - U.L.F.) en USD |
| Cobre      | REAL        | Precio del Cobre (Libras Finas - L.F) en USD |

Unidades de Medida

**L.F. (Libras Finas)** → Unidad utilizada para Zinc, Estaño, Plomo y Cobre.

**O.T. (Onzas Troy)** → Unidad utilizada para Oro y Plata.

**T.M.F. (Toneladas Métricas Finas)** → Unidad utilizada para Antimonio.

**U.L.F. (Unidades Libras Finas)** → Unidad utilizada para Wólfram.


## ⚠️ Notas 
Fuente: https://mineria.gob.bo/revista/pdf/20170817-10-15-28.pdf
Los valores están expresados en Dólares Americanos (USD).

La tabla almacena datos reales y puede actualizarse con nuevos valores en el futuro.


# Tabla: pbi_tipo_gasto_precio_constante 
# importante (En miles de bolivianos de 1990)
Fuente: https://www.ine.gob.bo/index.php/estadisticas-economicas/pib-y-cuentas-nacionales/producto-interno-bruto-anual/serie-historica-del-producto-interno-bruto/

Explicación de las Columnas:
Año (INTEGER PRIMARY KEY)

Descripción: Año al que corresponde el dato.
Función: Clave primaria, asegura unicidad y orden cronológico.
Ejemplo: 1990, 2022.
Gastos_Consumo (REAL)

Descripción: Gasto total en consumo, incluyendo consumo privado y público.
Función: Refleja el nivel de demanda interna.
Ejemplo: 4925441 millones de bolivianos de 1990.
Formacion_Capital (REAL)

Descripción: Inversión en formación bruta de capital fijo (ej. maquinaria, infraestructura).
Función: Indica el nivel de inversión en la economía, esencial para el crecimiento a largo plazo.
Ejemplo: 673879 millones de bolivianos de 1990.
Exportacion_Bienes_Servicios (REAL)

Descripción: Valor total de exportaciones de bienes y servicios.
Función: Mide la demanda externa y el ingreso de divisas.
Ejemplo: 918926 millones de bolivianos de 1990.
Importacion_Bienes (REAL)

Descripción: Valor total de importaciones de bienes y servicios.
Función: Mide la demanda de productos externos, afecta el saldo comercial.
Ejemplo: 882169 millones de bolivianos de 1990.
PIB_Real_Base_1990 (REAL)

Descripción: PIB real ajustado a precios constantes de 1990.
Función: Permite medir el crecimiento económico eliminando el efecto de la inflación.
Ejemplo: 5636077 millones de bolivianos de 1990.

# Tabla: tasa_crecimiento_pib
# importante (en porcentaje)
Explicación de las Columnas:
Año (INTEGER PRIMARY KEY)

Crecimiento (REAL)
Descripción: Tasa de crecimiento del PIB real respecto al año anterior.
Función: Indica el desempeño económico en términos porcentuales.
Ejemplo: 4.5 (representa un 4.5% de crecimiento).

fuente:INE

# Tabla: balanza_comercial
# importante (valores en millones de dolares)
columnas: Año, EXPORTACIONES ,MPORTACIONES, SALDO COMERCIAL
fuente: INE

# Tabla: PIB_Real_Gasto
# importante (valores en En millones de bolivianos de 1990)
columnas: año, gastos_consumo,formacion_capital, exportacion_bienes_servicios, importacion_bienes, pib_real_base_1990
fuente: INE

# Tabla: grado_de_apertura
# importante (valores en porcentaje)
# importante formula para obtenerlo (X+M) /PIB(%)
columnas: año, grado
fuente: INE

# Tabla: participacion_x_m_pib
# importante (valores en porcentaje)
# importante formula para obtenerlo X: X/PIB y M: M/PIB
columnas: año, X, M
fuente: INE

# Tabla: Reservas_oro_divisas  
# importante (valores en millones de dolares)
columnas: año, Reservas_Totales
fuente: INE

# Tabla: exp_trad_no_trad
# importante (valores en porcentaje)
columnas: 
año
exp_trad Exportaciones Tradicionales (% del total)
exp_no_trad Exportaciones No Tradicionales (% del total)

fuente:ine

# Tabla: exportaciones_totales
# Importante: (valores en millones de dólares)

Columnas:
Año (INTEGER PRIMARY KEY)
Productos_Tradicionales (REAL)
Función: Representa la cantidad exportada de productos tradicionales como minerales y productos agroindustriales.
Productos_No_Tradicionales (REAL)
Función: Representa la cantidad exportada de productos industriales y manufacturados.
Total_Valor_Oficial (REAL)
Función: Refleja la suma de productos tradicionales y no tradicionales exportados.
Fuente: INE

# Tabla: participacion_hidrocarburos_minerales_exportaciones_tradicionales
# Importante: (valores en porcentaje)

Explicación de las Columnas:
Año (INTEGER PRIMARY KEY)
Minerales (REAL)
Función: Indica la relevancia de los minerales dentro de las exportaciones tradicionales en un año determinado.
Hidrocarburos (REAL)
Función: Muestra el peso de los hidrocarburos en las exportaciones tradicionales.
Fuente: INE

# tabla participacion_gas_hidrocarburos_total_exportaciones_hidrocarburos
# importante: valores en porcentaje
Año (INTEGER PRIMARY KEY): Año de referencia.
Exportacion_Gas (REAL): Porcentaje de exportación de gas sobre el total de hidrocarburos.
Otros_Hidrocarburos (REAL): Porcentaje de otros hidrocarburos en la exportación total de hidrocarburos.
Fuente: INE.

# tabla composicion_importaciones_uso_destino
# Importante: (Valores en millones de dólares CIF)

Explicación de la tabla:
Año (INTEGER PRIMARY KEY): Año de referencia.
Bienes_Consumo (REAL): Valor de importaciones de bienes de consumo.
Materias_Primas_Productos_Intermedios (REAL): Valor de importaciones de materias primas y productos intermedios.
Bienes_Capital (REAL): Valor de importaciones de bienes de capital.
Diversos (REAL): Otras importaciones.
Total_Valor_Oficial_CIF (REAL): Total de las importaciones oficiales (CIF).
Fuente: INE

Desde el 2016 datos preliminares

# tabla participacion_composicion_importaciones_uso_destino 
# Importante: (Valores en porcentaje)

Explicación de las Columnas:
Año (INTEGER PRIMARY KEY): Año de referencia.
Bienes_Consumo (REAL): Porcentaje de importaciones de bienes de consumo respecto al total.
Materias_Primas_Productos_Intermedios (REAL): Porcentaje de importaciones de materias primas y productos intermedios sobre el total.
Bienes_Capital (REAL): Porcentaje de importaciones de bienes de capital sobre el total.
Diversos (REAL): Porcentaje de otras importaciones no categorizadas sobre el total.
Total_CIF (REAL): Total del valor CIF expresado siempre en 100%.
fuente:INE

Desde el 2016 datos preliminares