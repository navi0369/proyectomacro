# Guía para Generar Gráficas de Barras Apiladas (Barplot) - Serie Completa

Esta guía detalla el proceso específico para crear gráficas de barras apiladas utilizando las utilidades del proyecto Macro Bolivia, basada en el análisis del notebook `participacion_pib_rama_de_actividad.ipynb`.

## 📊 ¿Cuándo usar Gráficas de Barras Apiladas?

Las gráficas de barras apiladas son ideales para:
- **Composiciones porcentuales**: Mostrar cómo se distribuyen los componentes de un total (ej. participación sectorial en PIB)
- **Evolución de estructura**: Visualizar cambios en la composición a lo largo del tiempo
- **Comparación de partes vs todo**: Analizar la importancia relativa de cada componente
- **Series que suman 100%**: Participaciones, composiciones, distribuciones

## 🚀 Proceso Paso a Paso para Barplot

### 1. Configuración Inicial Específica

```python
# ───────────────────────────── IMPORTS ──────────────────────────────
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os
import numpy as np
import sys

# IMPORTANTE: Importación correcta para barplot
from func_auxiliares.config import *
from func_auxiliares.graficos_utils import (
    set_style,                    # Estilo corporativo
    plot_stacked_bar,            # 🔑 Función principal para barras apiladas
    add_hitos_barras,            # 🔑 Hitos específicos para barplot
    add_cycle_means_barras,      # 🔑 Medias por ciclo para barplot
    adjust_cycles,               # Ajustar ciclos al DataFrame
)

# Configuración de salida
OUTPUT_DIR = ASSETS_DIR / "serie_completa" / "[nombre_de_indicador]"
os.makedirs(OUTPUT_DIR, exist_ok=True)
set_style()
```

### 2. Carga y Preparación de Datos para Composiciones

```python
# ── Carga de datos ────────────────────────────────────────────
with sqlite3.connect(str(DB_PATH)) as conn:
    df = pd.read_sql_query("SELECT * FROM [nombre_tabla]", conn)

df.set_index("año", inplace=True)

# ── Creación de agregados (si es necesario) ──────────────────
# Ejemplo: combinar categorías relacionadas
df["servicios_y_finanzas"] = df["comercio_finanzas"] + df["servicios"] + df["propiedad_vivienda"]
df.drop(columns=["comercio_finanzas", "servicios", "propiedad_vivienda"], inplace=True)

# ── Definir componentes a graficar ───────────────────────────
componentes = [
    ("agropecuario", "Agropecuario"),
    ("mineria", "Minería"),
    ("petroleo_crudo_y_gas_natural", "Hidrocarburos"),
    ("industria_manufacturera", "Industria Manufacturera"),
    ("construcciones", "Construcción"),
    ("energia", "Energía"),
    ("transportes", "Transporte"),
    ("servicios_y_finanzas", "Servicios y Finanzas"),
    ("gobierno_general", "Gobierno General"),
]

# ── Extraer columnas para cálculos ───────────────────────────
cols = [col for col, _ in componentes]
```

### 3. 🔑 Cálculo de Porcentajes (Paso Crítico para Barplot)

```python
# ── Conversión a porcentajes (suma = 100% por año) ───────────
pct = df[cols].div(df[cols].sum(axis=1), axis=0) * 100

# Verificación: cada fila debe sumar 100%
print("Verificación de porcentajes:")
print(pct.sum(axis=1).round(2))  # Debe mostrar ~100.0 para cada año
```
Esto se debe realizar solo cuando los datos originales no estan en porcentaje, para confirmar eso se debe revisar la información de tabla en la categoria 'unidad base'.
### 4. Preparación de Ciclos y Estadísticas

```python
# ── Ajustar ciclos al DataFrame actual ───────────────────────
cycles_adj = adjust_cycles(df, CYCLES)

# ── Calcular estadísticas por ciclo (sobre porcentajes) ──────
cycle_stats = {
    name: pct.loc[sl, cols].mean().to_dict()
    for name, sl in cycles_adj.items()
}
```

### 5. 🎯 Configuración de Offsets Específicos para Barplot

Los barplot requieren configuraciones especiales diferentes a los gráficos de línea:

```python
# ── A) Offsets para hitos verticales en barplot ──────────────
hitos_offset = {
    1952: (0, 1),     # (desplazamiento_x, altura_relativa)
    1956: (0, 1),
    1970: (0, 1),
    1982: (0, 1),
    1985: (0, 1),
    2001: (0, 1),
    2006: (0, 1),
    2014: (0, 1)
}

# ── B) Posición horizontal del texto de hitos ────────────────
hitos_text_x = {
    1952: 1.9,        # Posición X del texto del hito
    1956: 6,
    1970: 5,
    1982: 1.5,
    1985: 6,
    2001: 2.5,
    2006: 5,
    2014: 5
}

# ── C) Offsets para medias por ciclo (específico por ciclo y componente) ──
MEAN_OFFSETS_BY_NAME = {
    "Crisis 52-55": {
        'componente1': (0.0, 12.0),    # (dx, dy) para cada componente
        'componente2': (0.0, 14.5),
    },
    "Expansión 56-69": {
        'componente1': (0.0, 14.5),
        'componente2': (0.0, 15.0),
    },
    # ... continuar para cada ciclo
}

# ── D) Componentes a excluir de anotaciones de medias ────────
SKIP_MEANS_BY_NAME = {
    "Crisis 52-55": {'energia'},          # No anotar 'energia' en este ciclo
    "Expansión 56-69": {'energia'},
    "Recesión 70-81": {'energia'},
    # ... continuar para cada ciclo donde quieras omitir componentes
}
```

### 6. 🎨 Generación del Gráfico de Barras Apiladas

```python
# ── Crear el gráfico base de barras apiladas ─────────────────
fig, ax = plot_stacked_bar(
    pct,                          # DataFrame con porcentajes
    series=componentes,           # Lista de tuplas (columna, etiqueta)
    title="[TÍTULO DEL GRÁFICO]",
    legend_ncol=6,               # Número de columnas en la leyenda
    figsize=(14, 8),             # Tamaño de la figura (opcional)
    xlabel="Año",                # Etiqueta del eje X (opcional)
    ylabel="Porcentaje (%)"      # Etiqueta del eje Y (opcional)
)
```

### 7. 🔧 Adición de Elementos Específicos para Barplot

```python
# ── A) Líneas verticales de hitos (específicas para barplot) ─
add_hitos_barras(
    ax, 
    df.index,           # Índice temporal (años)
    hitos_v,            # Diccionario de hitos de config.py
    hitos_offset,       # Offsets verticales
    hitos_text_x        # Posiciones horizontales del texto
)

# ── B) Medias por ciclo (específicas para barplot) ───────────
add_cycle_means_barras(
    ax,
    index=list(df.index),        # Secuencia de años
    cycle_slices=cycles_adj,     # Diccionario nombre → slice
    cycle_stats=cycle_stats,     # Diccionario nombre → {col: media}
    cols=cols,                   # Orden de apilado de componentes
    offsets=MEAN_OFFSETS_BY_NAME,  # Offsets específicos (opcional)
    skip=SKIP_MEANS_BY_NAME        # Componentes a omitir (opcional)
)
```

### 8. Finalización y Guardado

```python
# ── Finalizar y guardar ──────────────────────────────────────
plt.tight_layout()

# Guardar en formato PNG de alta resolución
out_path = os.path.join(OUTPUT_DIR, "[nombre_archivo].png")
plt.savefig(out_path, dpi=300)
plt.show()

print(f"Gráfico guardado en: {out_path}")
```

## 📚 Variantes de Configuración

### Variante 1: Gráfico con Crisis (Detallado)

```python
# Usar CYCLES estándar para mostrar todos los períodos
cycles_adj = adjust_cycles(df, CYCLES)

# Configurar hitos detallados
hitos_to_use = hitos_v  # Todos los hitos principales

# Filename
filename = "grafico_con_crisis.png"
```

### Variante 2: Gráfico por Períodos Estructurales (Simplificado)

```python
# Usar CYCLES_PERIODOS para vista macro
cycles_periodos = adjust_cycles(df, CYCLES_PERIODOS)
cycle_stats_periodos = {
    name: pct.loc[sl, cols].mean().to_dict()
    for name, sl in cycles_periodos.items()
}

# Hitos simplificados (solo cambios estructurales)
hitos_offset_periodos = {
    1952: (0, 1),
    1985: (0, 1),
    2006: (0, 1),
}

hitos_text_x_periodos = {
    1952: 15,
    1985: 10,
    2006: 10
}

# Usar hitos_v_periodos en lugar de hitos_v
add_hitos_barras(ax, df.index, hitos_v_periodos, hitos_offset_periodos, hitos_text_x_periodos)

# Filename
filename = "grafico_periodos_estructurales.png"
```

## 🔍 Diferencias Clave vs Gráficos de Línea

### Funciones Específicas para Barplot
| Función | Líneas | Barplot |
|---------|--------|---------|
| **Gráfico base** | `init_base_plot()` | `plot_stacked_bar()` |
| **Hitos** | `add_hitos()` | `add_hitos_barras()` |
| **Medias** | `add_cycle_means_multi()` | `add_cycle_means_barras()` |
| **Participaciones** | `add_participation_cycle_boxes()` | *Incorporado en barplot* |

### Configuración de Datos
| Aspecto | Líneas | Barplot |
|---------|--------|---------|
| **Datos** | Valores absolutos | **Porcentajes (suma=100%)** |
| **Transformación** | `df[cols]` | `df[cols].div(df[cols].sum(axis=1), axis=0) * 100` |
| **Validación** | Rangos coherentes | **Suma por fila = 100%** |

### Offsets Específicos
| Tipo | Líneas | Barplot |
|------|--------|---------|
| **Hitos** | `{año: altura_relativa}` | `{año: (dx, dy)}` + `hitos_text_x` |
| **Medias** | `{ciclo: (x, y)}` | `{ciclo: {componente: (dx, dy)}}` |
| **Estructura** | Por ciclo | **Por ciclo Y por componente** |

## 💡 Consejos Específicos para Barplot

### Preparación de Datos
1. **Verificar integridad**: Asegurar que `pct.sum(axis=1)` sea siempre ~100%
2. **Agregación lógica**: Combinar categorías pequeñas en "Otros" si es necesario
3. **Orden de componentes**: Colocar los más importantes primero en la lista `componentes`

### Configuración Visual
1. **Colores semánticamente apropiados**: 
   - Sectores primarios: tonos verdes/marrones
   - Industria: tonos azules
   - Servicios: tonos naranjas/amarillos
   - Gobierno: tonos grises

2. **Leyenda optimizada**:
   - Usar `legend_ncol` para distribución horizontal
   - Considerar ubicación `'upper center'` para leyendas largas

3. **Offsets de medias**:
   - Ajustar por altura de cada segmento
   - Evitar superposición con valores pequeños
   - Usar `skip` para componentes menores a ~2-3%

### Validación Final
1. **Coherencia temporal**: Verificar transiciones lógicas entre años
2. **Legibilidad**: Comprobar que todos los textos sean legibles
3. **Suma de verificación**: Confirmar que porcentajes sumen 100% visualmente

## 🛠️ Solución de Problemas Comunes

### Error: "Las barras no suman 100%"
```python
# Verificar cálculo de porcentajes
print("Sumas por año:")
print(pct.sum(axis=1))
# Debe mostrar valores cercanos a 100.0

# Si hay diferencias, verificar datos originales
print("Datos originales (últimos 5 años):")
print(df[cols].tail())
```

### Error: "Textos de medias superpuestos"
```python
# Ajustar offsets en MEAN_OFFSETS_BY_NAME
# Aumentar espaciamiento vertical (dy) para componentes problemáticos
MEAN_OFFSETS_BY_NAME = {
    "Ciclo problemático": {
        'componente1': (0.0, 5.0),   # Mover hacia abajo
        'componente2': (0.0, 15.0),  # Mover hacia arriba
    }
}
```

### Error: "Hitos no aparecen correctamente"
```python
# Verificar que hitos_text_x tenga valores apropiados
# Para barplot, los valores deben estar en rango [0, max_height]
print("Altura máxima del gráfico:", pct.sum(axis=1).max())
# Ajustar hitos_text_x en consecuencia
```

## 📋 Checklist para Barplot

### Antes de Ejecutar
- [ ] Datos convertidos a porcentajes con `div().sum(axis=1) * 100`
- [ ] Verificar que `pct.sum(axis=1)` ≈ 100 para todos los años
- [ ] Definir `componentes` en orden lógico (más importante primero)
- [ ] Configurar `hitos_offset` Y `hitos_text_x` para barplot

### Durante el Desarrollo
- [ ] Usar `plot_stacked_bar()` en lugar de `init_base_plot()`
- [ ] Usar `add_hitos_barras()` en lugar de `add_hitos()`
- [ ] Usar `add_cycle_means_barras()` en lugar de `add_cycle_means_multi()`
- [ ] Configurar `MEAN_OFFSETS_BY_NAME` por ciclo Y componente

### Antes de Finalizar
- [ ] Verificar que la leyenda sea legible y bien distribuida
- [ ] Comprobar que no hay textos superpuestos
- [ ] Validar que los colores sean semánticamente apropiados
- [ ] Confirmar que las medias por ciclo sean correctas
- [ ] Guardar en alta resolución (dpi=300)

## 🔗 Referencias Específicas

- **Función principal**: `plot_stacked_bar()` en `func_auxiliares.graficos_utils`
- **Configuración de hitos**: `hitos_v`, `hitos_v_periodos` en `func_auxiliares.config`
- **Ciclos económicos**: `CYCLES`, `CYCLES_PERIODOS` en `func_auxiliares.config`
- **Ejemplo de referencia**: `notebooks/tesis/serie_completa/pib/participacion_pib_rama_de_actividad.ipynb`

Esta guía cubre todos los aspectos específicos para crear gráficas de barras apiladas profesionales siguiendo los patrones establecidos en el proyecto.
