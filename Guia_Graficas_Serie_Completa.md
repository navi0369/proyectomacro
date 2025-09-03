# Guía Completa para Generar Gráficas de Serie Completa
Importante: tu objetivo principal es solo generar el codigo para el notebook, solo limitate a eso.

Esta guía detalla el proceso completo para crear gráficas de series económicas completas utilizando las utilidades del proyecto Macro Bolivia. Está basada en el análisis de todos los notebooks existentes en `notebooks/tesis/serie_completa/`.

## 📁 Estructura de Archivos

### Archivos de Utilidades Centrales
- **`func_auxiliares/config.py`**: Configuración global, ciclos económicos, años de hitos
- **`func_auxiliares/graficos_utils.py`**: Funciones de graficación y utilidades
- **`db/proyectomacro.db`**: Base de datos SQLite con todas las series económicas

### Estructura de Directorios de Salida
```
assets/tesis/serie_completa/
├── balanza_comercial/
├── exportaciones/
├── pib/
├── inflacion_acumulada/
├── minerales/
└── [indicador_específico]/
```

## 🚀 Proceso Paso a Paso

### 1. Configuración Inicial del Notebook

```python
# ───────────────────────────── IMPORTS ──────────────────────────────
import os
import sys
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# IMPORTANTE: Importación correcta de las funciones auxiliares
from func_auxiliares.graficos_utils import (
    set_style,                          # Estilo corporativo
    init_base_plot,                     # Configuración base del gráfico
    add_hitos,                          # Líneas verticales de hitos
    add_cycle_means_multi,              # Medias por ciclo
    add_year_value_annotations,         # Anotaciones de valores por año
    add_period_growth_annotations_multi,# Tasas de crecimiento por período
    add_participation_cycle_boxes,      # Cajas de participación (para gráficos apilados)
    adjust_annot_years,                 # Ajustar años de anotación al DataFrame
    adjust_cycles,                      # Ajustar ciclos al DataFrame
    adjust_periods,                     # Ajustar períodos al DataFrame
    get_df                              # Función helper para cargar datos
)

from func_auxiliares.config import (
    DB_PATH,                            # Ruta a la base de datos
    CYCLES,                             # Diccionario de ciclos económicos
    CYCLES_SIN_CRISIS,                  # Ciclos sin crisis (opcional)
    CYCLES_PERIODOS,
    ASSETS_DIR,                         # Ciclos por períodos estructurales (opcional)
    annot_years,                        # Lista de años para anotaciones
    annot_years_sin_crisis,             # Años sin crisis (opcional)
    annot_years_periodos,               # Años por períodos (opcional)
    periodos_tasas,                     # Períodos para calcular tasas
    periodos_tasas_sin_crisis,          # Períodos sin crisis (opcional)
    periodos_tasas_periodos,            # Períodos estructurales (opcional)
    hitos_v,                            # Diccionario de hitos verticales
    hitos_v_sin_crisis,                 # Hitos sin crisis (opcional)
    hitos_v_periodos                    # Hitos por períodos (opcional)
)

# ─────────────────────── 1. CONFIGURACIÓN GENERAL ───────────────────
output_dir = ASSETS_DIR/ "serie_completa"/ "[nombre_indicador]"
os.makedirs(output_dir, exist_ok=True)

set_style()  # Aplica el estilo corporativo unificado
```

### 2. Carga de Datos

#### Opción A: Conexión Directa a SQLite
```python
# ───────────────────────── 2. CARGA DE DATOS ────────────────────────
with sqlite3.connect(str(DB_PATH)) as conn:
    df = (
        pd.read_sql(
            "SELECT * FROM [nombre_tabla]",  # Cambiar por tu tabla
            conn,
            index_col="año"
        )
        .sort_index()
    )
```

#### Opción B: Usando la Función Helper
```python
# Alternativa usando get_df (más simple)
query = "SELECT * FROM [nombre_tabla]"
df = get_df(query, str(DB_PATH), rename={'columna_vieja': 'columna_nueva'})
```

#### Transformaciones Comunes de Datos
```python
# Convertir miles a millones (común en datos económicos)
valor_cols = [c for c in df.columns if c.endswith('_valor')]
df[valor_cols] = df[valor_cols] / 1000

# Crear columnas calculadas
df["total"] = df[valor_cols].sum(axis=1)
df["participacion"] = df["componente"] / df["total"] * 100

# Filtrar años específicos si es necesario
df = df.loc[df.index >= 1985]  # Ejemplo: desde 1985
```

### 3. Definición de Componentes y Configuración Visual

```python
# ──────────────── 3. COMPONENTES Y PREPARACIÓN ──────────────────────
# Definir las series a graficar (tuplas de columna_df, etiqueta_display)
componentes = [
    ("exportaciones", "Exportaciones"),
    ("importaciones", "Importaciones"),
    ("saldo_comercial", "Saldo comercial"),
]

# Extraer solo los nombres de columnas
cols_componentes = [col for col, _ in componentes]

# Definir colores para cada serie
colors = {
    "exportaciones": "green",
    "importaciones": "red", 
    "saldo_comercial": "steelblue",
}

# Abreviaciones para anotaciones (texto más corto)
abbr_map = {
    "exportaciones": "X",
    "importaciones": "M",
    "saldo_comercial": "SC",
}
```

### 4. Preparación de Ciclos y Períodos

```python
# ──────────────── 4. PREPARACIÓN DE CICLOS Y PERÍODOS ────────────────
# Ajustar configuraciones globales al DataFrame actual
annotate_years = adjust_annot_years(df, annot_years)
cycles = adjust_cycles(df, CYCLES)
periods = adjust_periods(df, periodos_tasas)

# Calcular estadísticas por ciclo (medias)
cycle_stats = {
    name: df.loc[period, cols_componentes].mean().to_dict()
    for name, period in cycles.items()
}
```

### 5. Configuración de Posicionamiento (Offsets)

Esta es la parte más importante para lograr gráficas limpias y profesionales:

```python
# ───────────── 5. OFFSETS Y UTILIDADES (POSICIONAMIENTO) ────────────

# A) Offsets para anotaciones de valores por año y serie
annotation_offsets = {
    "exportaciones": {
        1952: (0,   660),    # (desplazamiento_x, desplazamiento_y)
        1956: (0,   660),
        1970: (0,   660),
        1982: (0,   920),
        1985: (0,   820),
        2001: (0,  1920),
        2006: (-1.5, 400),
        2014: (-3.2, -400),
        2024: (-0.8, -800),
    },
    "importaciones": {
        1952: (0,   300),
        1956: (0,   300),
        1970: (0,   300),
        1982: (0,   720),
        1985: (0,   350),
        2001: (0,  1040),
        2006: (1.2, -600),
        2014: (4,     0),
        2024: (0.8, -1200),
    },
    # ... más series
}

# B) Offsets para líneas verticales de hitos
hitos_offset = {year: 0.8 for year in hitos_v}  # Altura relativa uniforme

# C) Offsets para medias por ciclo
medias_offsets = {
    "Expansión 56-69": (1958, 0.92),    # (año_centro, altura_relativa)
    "Recesión 70-81":  (1972, 0.92),
    "Expansión 85-00": (1988, 0.92),
    "Expansión 06-14": (2006, 0.92),
    "Recesión 15-24":  (2018, 0.92),
}

# D) Offsets para tasas de crecimiento por período
tasas_offsets = {
    "1956-1969": (1962, 0.83),
    "1970-1981": (1975, 0.83),
    "1985-2000": (1992, 0.83),
    "2006-2014": (2009, 0.83),
    "2015-2024": (2019, 0.83),
}

# E) Offsets para participaciones (solo en gráficos apilados)
participation_offsets = {
    "1956-1969": (1962, 0.65),
    "1970-1981": (1975, 0.65),
    "1985-2000": (1992, 0.65),
    "2006-2014": (2009, 0.65),
    "2015-2024": (2019, 0.65),
}
```

### 6. Generación del Gráfico Base

```python
# ────────────────────────── 6. GRÁFICO BASE ──────────────────────────
fig, ax = init_base_plot(
    df=df,
    series=componentes,           # Lista de tuplas (columna, etiqueta)
    colors=colors,                # Diccionario de colores
    title=f"[Título del Gráfico] ({df.index.min()}–{df.index.max()})",
    xlabel="Año",
    ylabel="[Unidad de medida]",
    source_text="Fuente: [Fuente de datos]"
)
```

### 7. Adición de Elementos Gráficos

```python
# ────────────────────── 7. ELEMENTOS GRÁFICOS ADICIONALES ────────────

# A) Líneas verticales de hitos históricos
add_hitos(ax, df.index, hitos_v, hitos_offset)

# B) Anotaciones de valores en años específicos
add_year_value_annotations(
    ax, df, annotate_years,
    cols_componentes, annotation_offsets, colors,
    arrow_lw=0.4,                # Grosor de flecha                 # Tamaño defuente
)

# C) Medias por ciclo económico
add_cycle_means_multi(
    ax,
    cycle_stats,
    medias_offsets,
    abbr_map,
    colors,
    line_spacing=50              # Espaciado entre líneas
)

# D) Tasas de crecimiento por período
add_period_growth_annotations_multi(
    ax, df, periods,
    cols_componentes,
    tasas_offsets,
    colors,
    abbr_map,          # Decimales en porcentajes
)

# E) Cajas de participación (solo para gráficos apilados)
# add_participation_cycle_boxes(
#     ax, df, periods,
#     componentes,
#     total_col,
#     ofssets,
#     abbr_map,
#     colors
# )
```

### 8. Finalización y Guardado

```python
# ────────────────────────── 8. FINALIZACIÓN ──────────────────────────
plt.tight_layout()

# Guardar en múltiples formatos
filename_base = f"{output_dir}/[nombre_archivo]"
fig.savefig(f"{filename_base}.png", dpi=300, bbox_inches="tight")

plt.show()
plt.close()  # IMPORTANTE: Cerrar la figura para liberar memoria
```

## 📈 Patrón Estándar: Dos Gráficas por Serie

La mayoría de series completas incluyen **dos gráficas complementarias**:

### 1. Gráfica Principal (Con Crisis)
- **Configuración**: Usa `CYCLES`, `annot_years`, `periodos_tasas`, `hitos_v`
- **Enfoque**: Análisis detallado de ciclos económicos incluyendo crisis
- **Períodos**: 8 ciclos específicos (Crisis 52-55, Expansión 56-69, etc.)
- **Archivo**: `[nombre_serie]_ciclos.png`

### 2. Gráfica de Períodos Estructurales
- **Configuración**: Usa `CYCLES_PERIODOS`, `annot_years_periodos`, `periodos_tasas_periodos`, `hitos_v_periodos`
- **Enfoque**: Análisis de largo plazo por modelo económico
- **Períodos**: 3 grandes etapas estructurales
- **Archivo**: `[nombre_serie]_periodos.png`

### Implementación del Patrón Dual

```python
# ═══════════════════════════════════════════════════════════════════
# PRIMERA GRÁFICA: CICLOS CON CRISIS
# ═══════════════════════════════════════════════════════════════════
annotate_years = adjust_annot_years(df, annot_years)
cycles_stats = {n: df.loc[s, cols_componentes].mean().to_dict()
                for n, s in adjust_cycles(df, CYCLES).items()}
periodos = adjust_periods(df, periodos_tasas)

# ... offsets específicos para ciclos ...
annotation_offsets = { ... }
medias_offsets = { ... }
tasas_offsets = { ... }

# Construcción del gráfico principal
fig, ax = init_base_plot(
    df, componentes, colors,
    f"[NOMBRE_SERIE] ({df.index.min()}–{df.index.max()}) — CICLOS CON CRISIS",
    "Año", "[Unidad]", source_text="Fuente: [...]"
)
add_hitos(ax, df.index, hitos_v, hitos_offset)
add_cycle_means_multi(ax, cycles_stats, medias_offsets, abbr_map, colors)
add_year_value_annotations(ax, df, annotate_years, cols_componentes, annotation_offsets, colors)
add_period_growth_annotations_multi(ax, df, periodos, cols_componentes, tasas_offsets, colors, abbr_map)

plt.savefig(os.path.join(output_dir, "[nombre_serie]_ciclos.png"))
plt.show()
plt.close()

# ═══════════════════════════════════════════════════════════════════
# SEGUNDA GRÁFICA: PERÍODOS ESTRUCTURALES  
# ═══════════════════════════════════════════════════════════════════
annotate_years_periodos = adjust_annot_years(df, annot_years_periodos)
cycles_stats_periodos = {n: df.loc[s, cols_componentes].mean().to_dict()
                        for n, s in adjust_cycles(df, CYCLES_PERIODOS).items()}
periodos_periodos = adjust_periods(df, periodos_tasas_periodos)

# ... offsets específicos para períodos estructurales ...
annotation_offsets_periodos = { ... }
medias_offsets_periodos = { ... }
tasas_offsets_periodos = { ... }

# Construcción del gráfico de períodos
fig, ax = init_base_plot(
    df, componentes, colors,
    f"[NOMBRE_SERIE] ({df.index.min()}–{df.index.max()}) — Períodos Económicos",
    "Año", "[Unidad]", source_text="Fuente: [...]"
)
add_hitos(ax, df.index, hitos_v_periodos, hitos_offset_periodos)
add_cycle_means_multi(ax, cycles_stats_periodos, medias_offsets_periodos, abbr_map, colors)
add_year_value_annotations(ax, df, annotate_years_periodos, cols_componentes, annotation_offsets_periodos, colors)
add_period_growth_annotations_multi(ax, df, periodos_periodos, cols_componentes, tasas_offsets_periodos, colors, abbr_map)

plt.savefig(os.path.join(output_dir, "[nombre_serie]_periodos.png"))
plt.show()
plt.close()
```

## 📊 Tipos de Gráficos Específicos

### Gráfico de Líneas Simple
```python
# Para una sola serie
componentes = [("pib_real", "PIB Real")]
colors = {"pib_real": "#1f77b4"}
```

### Gráfico de Líneas Múltiples
```python
# Para múltiples series en el mismo eje
componentes = [
    ("exportaciones", "Exportaciones"),
    ("importaciones", "Importaciones"),
]
colors = {
    "exportaciones": "green",
    "importaciones": "red",
}
```



## 🎨 Configuraciones Avanzadas

### Múltiples Gráficos (Variantes de Crisis)

```python
# GRÁFICO 1: Con crisis incluidas
cycles_crisis = adjust_cycles(df, CYCLES)
# ... configurar offsets para crisis ...

# GRÁFICO 2: Sin crisis
cycles_sin_crisis = adjust_cycles(df, CYCLES_SIN_CRISIS) 
# ... configurar offsets sin crisis ...

# GRÁFICO 3: Períodos estructurales
cycles_periodos = adjust_cycles(df, CYCLES_PERIODOS)
# ... configurar offsets por períodos ...
```

### Personalización de Estilos

```python
# Modificar parámetros específicos después de init_base_plot
ax.set_ylim(bottom=0)                    # Forzar inicio en 0
ax.grid(True, alpha=0.3)                 # Grid más sutil
ax.legend(loc='best', frameon=False)     # Leyenda sin marco

# Formatear ejes
ax.yaxis.set_major_formatter(
    plt.FuncFormatter(lambda x, p: f'{x:,.0f}')  # Formato con comas
)
```

## � Gráfica de Períodos Estructurales (Segunda Gráfica)

Muchas series completas incluyen una segunda gráfica que analiza los períodos estructurales de la economía boliviana: **Intervencionismo-estatal**, **Neoliberalismo** y **Neodesarrollismo**.

### Configuración Específica para Períodos Estructurales

```python
# ============================================================
# 2) PERÍODOS ESTRUCTURALES
# ============================================================
# Usar configuraciones específicas de config.py para períodos
annotate_years_periodos = adjust_annot_years(df, annot_years_periodos)
cycles_stats_periodos = {
    name: df.loc[period, cols_componentes].mean().to_dict()
    for name, period in adjust_cycles(df, CYCLES_PERIODOS).items()
}
periodos_periodos = adjust_periods(df, periodos_tasas_periodos)
```

### Offsets Específicos para Períodos Estructurales

```python
# Anotaciones de valores (ajustar según la serie específica)
annotation_offsets_periodos = {
    "serie_principal": {
        1952: (0, -250),    # Inicio intervencionismo-estatal
        1985: (0, -300),    # Inicio neoliberalismo  
        2006: (-2, 150),    # Inicio neodesarrollismo
        2014: (3.5, -400),  # Punto medio/final neodesarrollismo
        2023: (0, -380),    # Final de serie
    },
    # Agregar más series si es necesario...
}

# Hitos verticales para períodos estructurales
hitos_offset_periodos = {year: 0.8 for year in hitos_v_periodos}

# Medias por período estructural
medias_offsets_periodos = {
    'Intervensionismo-estatal 52-84': (1957, 1),      # Posición central del período
    'Neoliberalismo 85-05': (1986, 1),                # Posición central del período
    'Neodesarrollismo 06-24': (2006, 1.09),           # Inicio del período
}

# Tasas de crecimiento por período estructural
tasas_offsets_periodos = {
    '1952-1984': (1957, 0.83),    # Intervencionismo-estatal
    '1985-2005': (1986, 0.83),    # Neoliberalismo
    '2006-2023': (2006, 1.01),    # Neodesarrollismo (ajustar según datos disponibles)
}
```

### Construcción de la Gráfica de Períodos

```python
# Gráfico base con título específico para períodos
fig, ax = init_base_plot(
    df, componentes, colors,
    f"[NOMBRE_SERIE] ({df.index.min()}–{df.index.max()}) — Períodos Económicos",
    "Año", "[Unidad de medida]",
    source_text="Fuente: [Fuente específica]"
)

# Elementos gráficos específicos para períodos
add_hitos(ax, df.index, hitos_v_periodos, hitos_offset_periodos, line_kwargs={'lw':0.9})

add_cycle_means_multi(
    ax, cycles_stats_periodos, medias_offsets_periodos,
    abbr_map, colors, line_spacing=ax.get_ylim()[1]*0.03
)

add_year_value_annotations(
    ax, df, annotate_years_periodos, cols_componentes,
    annotation_offsets_periodos, colors, arrow_lw=0.5
)

add_period_growth_annotations_multi(
    ax, df, periodos_periodos, cols_componentes,
    tasas_offsets_periodos, colors, abbr_map
)

# Ajustar límites del eje Y según la serie
ax.set_ylim([valor_mínimo], df['serie_principal'].max()*1.15)

# Guardar con nombre específico para períodos
plt.savefig(os.path.join(output_dir, "[nombre_serie]_periodos.png"))
plt.show()
plt.close()
```

### Diferencias Clave con la Gráfica Principal

1. **Configuración de Ciclos**: Usa `CYCLES_PERIODOS` en lugar de `CYCLES`
2. **Años de Anotación**: Usa `annot_years_periodos` (típicamente: 1952, 1985, 2006, 2023)
3. **Hitos Verticales**: Usa `hitos_v_periodos` que marca los cambios estructurales
4. **Períodos de Cálculo**: Usa `periodos_tasas_periodos` para las tres grandes etapas
5. **Offsets Diferentes**: Posicionamiento específico para los tres períodos estructurales
6. **Nombre de Archivo**: Termina en `_periodos.png`

### Años Clave para Períodos Estructurales

- **1952**: Inicio del Intervencionismo-estatal (Revolución Nacional)
- **1985**: Transición al Neoliberalismo (Nueva Política Económica)  
- **2006**: Inicio del Neodesarrollismo (Gobierno de Evo Morales)
- **2014-2023**: Punto medio/final del Neodesarrollismo (según disponibilidad de datos)

### Consideraciones Especiales

- **Flexibilidad en Fechas**: El período de Neodesarrollismo puede ajustarse (2006-2014, 2006-2024) según disponibilidad de datos
- **Medias por Período**: Se calculan para períodos más largos que en la gráfica principal
- **Interpretación Económica**: Enfoque en cambios estructurales más que en ciclos coyunturales
- **Posicionamiento Visual**: Los offsets deben permitir clara distinción entre los tres períodos

## �🔧 Funciones Auxiliares Más Comunes

### `set_style()`
Aplica el estilo corporativo unificado (colores, fuentes, DPI, etc.)

### `init_base_plot()`
Crea el gráfico base con series, colores, títulos y leyenda

### `adjust_*()` functions
- `adjust_cycles()`: Ajusta ciclos económicos al rango de datos disponible
- `adjust_annot_years()`: Filtra años de anotación que existen en los datos  
- `adjust_periods()`: Ajusta períodos para cálculo de tasas

### `add_*()` functions
- `add_hitos()`: Líneas verticales para hitos históricos
- `add_year_value_annotations()`: Valores específicos en años clave
- `add_cycle_means_multi()`: Promedios por ciclo económico
- `add_period_growth_annotations_multi()`: Tasas de crecimiento por período
- `add_participation_cycle_boxes()`: Participaciones en gráficos apilados



Esta guía cubre todos los patrones identificados en los notebooks existentes. Para casos específicos, consultar los notebooks de referencia en la carpeta correspondiente.


<!-- 🔒 CONTRATO DE SALIDA (OBLIGATORIO)
Objetivo: primero crear la carpeta y el archivo .ipynb si no existe. Luego Generar TODO el código del gráfico en UNA sola celda de Jupyter por grafica y insertarlo en el archivo creado.

REGLAS:
1) Devuelve EXACTAMENTE un (1) bloque de código.

Contenido obligatorio del bloque:
- Imports y configuración
- Carga de datos
- Preparaciones/transformaciones
- Definiciones (componentes, colores, offsets)
- Cálculos de ciclos/períodos/anotaciones
- Construcción del gráfico + elementos
- Guardado (png) y plt.show()