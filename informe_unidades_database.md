# Informe de Análisis de Unidades - Base de Datos Proyecto Macro

## Resumen Ejecutivo

Este informe presenta un análisis completo de todas las unidades de medida utilizadas en la base de datos del Proyecto Macro, basado en el archivo de configuración `pages.yml`. Se identificaron **21 tipos únicos de unidades** distribuidas en **43 tablas** diferentes.

## Datos Generales

- **Total de tablas analizadas**: 43
- **Total de unidades únicas**: 21
- **Distribución**: Las unidades monetarias (tanto en bolivianos como dólares) representan el 67% del total de tablas

## Categorización de Unidades

### 1. Unidades Monetarias en Bolivianos (6 tipos únicos, 14 tablas)

| Unidad | Frecuencia | Observaciones |
|--------|------------|---------------|
| **Miles de bolivianos constantes de 1990** | 5 tablas | Unidad más común para datos deflactados |
| **Millones de bolivianos** | 5 tablas | Para grandes agregados económicos |
| **Bolivianos por dólar** | 1 tabla | Tipo de cambio nominal |
| **Bolivianos por dólar (Bs/USD)** | 1 tabla | Tipo de cambio con especificación |
| **Miles de bolivianos** | 1 tabla | Datos corrientes en escala media |
| **Miles de bolivianos (BOB)** | 1 tabla | Con código de moneda ISO |

**Análisis**: Predominan las unidades deflactadas (base 1990) para análisis de series temporales reales. Existe inconsistencia en la nomenclatura del tipo de cambio.

### 2. Unidades Monetarias en Dólares (5 tipos únicos, 15 tablas)

| Unidad | Frecuencia | Observaciones |
|--------|------------|---------------|
| **Millones de dólares** | 10 tablas | Unidad MÁS FRECUENTE en toda la base |
| **Miles de dólares** | 2 tablas | Para agregados menores |
| **Millones de dólares estadounidenses (USD)** | 1 tabla | Con especificación de moneda |
| **Millones de dólares (valor CIF frontera)** | 1 tabla | Específica para comercio exterior |
| **Dólares por barril** | 1 tabla | Precio de commodities |

**Análisis**: Los dólares son la unidad predominante (35% de todas las tablas), reflejando la dolarización parcial de la economía boliviana.

### 3. Unidades Porcentuales (6 tipos únicos, 10 tablas)

| Unidad | Frecuencia | Aplicación |
|--------|------------|------------|
| **Porcentaje** | 3 tablas | Tasas generales |
| **Porcentaje del PIB** | 3 tablas | Ratios fiscales y macroeconómicos |
| **Porcentaje del total** | 1 tabla | Composición general |
| **Porcentaje del total CIF** | 1 tabla | Estructura de importaciones |
| **Porcentaje del total de hidrocarburos** | 1 tabla | Sector hidrocarburos |
| **Porcentaje del total tradicional** | 1 tabla | Exportaciones tradicionales |

**Análisis**: Alta especificidad en los porcentajes, mostrando análisis detallado por sectores.

### 4. Otras Categorías

#### Índices (1 tipo, 1 tabla)
- **Índice (1990 = 100)**: Para series deflactadas con año base

#### Unidades Físicas (2 tipos, 2 tablas)
- **Toneladas finas**: Producción minera
- **Personas**: Variables demográficas

#### Unidades Especiales (1 tipo, 1 tabla)
- **US$ corrientes por habitante**: PIB per cápita

## Top 10 Unidades Más Frecuentes

| Ranking | Unidad | Frecuencia | % del Total |
|---------|--------|------------|-------------|
| 1 | Millones de dólares | 10 | 23.3% |
| 2 | Miles de bolivianos constantes de 1990 | 5 | 11.6% |
| 3 | Millones de bolivianos | 5 | 11.6% |
| 4 | Porcentaje | 3 | 7.0% |
| 5 | Porcentaje del PIB | 3 | 7.0% |
| 6 | Miles de dólares | 2 | 4.7% |
| 7-21 | Otras 15 unidades | 1 c/u | 34.8% |

## Distribución por Categorías

```
Monetarias (Dólares):    15 tablas (34.9%)
Monetarias (Bolivianos): 14 tablas (32.6%)
Porcentajes:             10 tablas (23.3%)
Físicas:                  2 tablas (4.7%)
Índices:                  1 tabla (2.3%)
Otras:                    1 tabla (2.3%)
```

## Hallazgos Importantes

### 1. **Inconsistencias de Nomenclatura**
- Existen duplicaciones en la descripción del tipo de cambio
- Algunas unidades incluyen códigos ISO, otras no
- Variabilidad en el nivel de detalle de las especificaciones

### 2. **Año Base Consistente**
- Todas las series deflactadas usan 1990 como año base
- Esto facilita las comparaciones temporales

### 3. **Predominio de Unidades Monetarias**
- El 67% de las tablas usan unidades monetarias
- Refleja la naturaleza macroeconómica del proyecto

### 4. **Especialización Sectorial**
- Los porcentajes muestran alta especialización por sectores
- Existe granularidad en la clasificación de comercio exterior

## Recomendaciones

### 1. **Estandarización de Nomenclatura**
```yaml
# Propuesta de estandarización
Tipo de Cambio: "Bolivianos por dólar (Bs/USD)"
Dólares con especificación: "Millones de dólares estadounidenses (USD)"
Constantes: "Miles de bolivianos constantes (base 1990)"
```

### 2. **Documentación de Metodología**
- Crear glosario de unidades con definiciones precisas
- Documentar métodos de deflactación para series constantes
- Especificar fuentes de tipos de cambio utilizados

### 3. **Validación de Consistencia**
- Implementar validaciones automáticas para detectar inconsistencias
- Crear alertas cuando se introduzcan nuevas unidades no estándar

## Conclusiones

La base de datos muestra una estructura bien organizada con **21 tipos de unidades** que cubren comprehensivamente los aspectos macroeconómicos de Bolivia. La predominancia de unidades monetarias (67% de las tablas) refleja adecuadamente el enfoque macroeconómico del proyecto.

**Fortalezas identificadas:**
- Uso consistente de año base 1990 para deflactación
- Cobertura completa de sectores económicos
- Granularidad apropiada en clasificaciones sectoriales

**Áreas de mejora:**
- Estandarización de nomenclatura para unidades similares
- Documentación más detallada de metodologías
- Implementación de validaciones automáticas

El análisis revela una base de datos robusta y bien estructurada que serve eficazmente para el análisis macroeconómico de la economía boliviana.

---

*Informe generado automáticamente a partir del análisis de pages.yml*  
*Fecha: $(date)*  
*Total de registros analizados: 43 tablas, 21 unidades únicas*
