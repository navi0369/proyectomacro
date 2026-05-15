# Skills de Notebooks — Proyectomacro (Gráficas de Barras)

Este archivo registra los skills disponibles para manipular y estandarizar notebooks `.ipynb` que contienen **gráficas de barras apiladas**.

---

## Skill: `grafica_periodos_barras`

**Propósito:** Modificar (o crear) un notebook para que contenga **una celda de código** enfocada en generar gráficas de barras apiladas de los **períodos estructurales** (`_periodos`), usando las constantes `CYCLES_PERIODOS` y `hitos_v_periodos` del `config.py` global, y las utilidades específicas para barras (`plot_stacked_bar`, `add_hitos_barras`, `add_cycle_means_barras`).

---

### Cuándo usarlo

- Cuando el usuario pide estandarizar una gráfica de barras apiladas (ej. participación porcentual).
- Cuando el notebook requiere la separación visual mediante líneas verticales de ciclos en un entorno de gráfico de barras.

---

### Procedimiento obligatorio

1. **Abrir / verificar el notebook** con `mcp_antigravity-nb_open_notebook`.
2. **Listar todas las celdas** con `mcp_antigravity-nb_list_cells`.
3. **Analizar la lógica previa**, si hay preprocesamiento de variables (cálculos de suma, divisiones por el PIB, etc.) **se deben mantener** en la celda principal.
4. **Editar o reemplazar la celda de código** insertando la lógica estandarizada del template siguiente.
5. **Ejecutar la celda** con `mcp_antigravity-nb_run_cell` para verificar que no hay errores.

---

### Template de la celda

```python
# ═══════════════════════════════════════════════════════════════════
# GRÁFICA DE PERÍODOS ESTRUCTURALES (BARRAS) — [NOMBRE_INDICADOR]
# ═══════════════════════════════════════════════════════════════════
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from func_auxiliares.graficos_utils import (
    set_style,
    plot_stacked_bar,
    add_hitos_barras,
    add_cycle_means_barras,
    adjust_cycles,
)

from func_auxiliares.config import (
    DB_PATH,
    ASSETS_DIR,
    CYCLES_PERIODOS,
    hitos_v_periodos,
)

# ─────────────────────── 1. CONFIGURACIÓN GENERAL ───────────────────
OUTPUT_DIR = ASSETS_DIR / "serie_completa" / "[nombre_indicador]"
os.makedirs(OUTPUT_DIR, exist_ok=True)
set_style()

# ─────────────────────────── 2. CARGA DE DATOS ──────────────────────
with sqlite3.connect(str(DB_PATH)) as conn:
    df = pd.read_sql("SELECT * FROM [nombre_tabla]", conn, index_col="año")

cycles_adj = adjust_cycles(df, CYCLES_PERIODOS)

# ⚠️ INCLUIR AQUÍ LÓGICA DE TRANSFORMACIÓN DE DATOS (si aplica)
# Ej: Convertir a participación porcentual
# pct = df[cols].div(df["pib_real_base_1990"], axis=0).multiply(100)
# Para la gráfica base usaremos data_plot como el DataFrame final.
data_plot = df 

# ──────────────── 3. COMPONENTES Y ESTADÍSTICAS ────────────
componentes = [
    ("[columna_1]", "[Etiqueta 1]"),
    ("[columna_2]", "[Etiqueta 2]"),
]
cols = [c for c, _ in componentes]

# Cálculo de estadísticas promedio por ciclo
cycle_stats = {
    name: data_plot.loc[sl, cols].mean().to_dict()
    for name, sl in cycles_adj.items()
}

# ───────────────────── 4. OFFSETS DE POSICIONAMIENTO ────────────────
hitos_offset = {
    1952: (0, 1),
    1985: (0, 1),
    2006: (0, 1),
    2015: (0, 1)
}
hitos_text_x = {
    1952: 12,
    1985: 8,
    2006: 5,
    2015: 5
}

# Offsets manuales para mover las anotaciones de la media de alguna columna
MEAN_OFFSETS_BY_NAME = {
    "INTERVENSIONISMO ESTATAL": {'[columna]': (0.0, 12.0)}, 
    "NEOLIBERALISMO":           {'[columna]': (0.0, 14.5)},
    "E.S.C.P (I)":              {'[columna]': (0.0, 12.0)},
    "E.S.C.P (II)":             {'[columna]': (0.0, 12.0)},
}

# Componentes de las que NO se quiere mostrar el promedio en el gráfico
SKIP_MEANS_BY_NAME = {
    "INTERVENSIONISMO ESTATAL": {'[columna_omitir]'}, 
    "NEOLIBERALISMO":           {'[columna_omitir]'},
    "E.S.C.P (I)":              {'[columna_omitir]'},
    "E.S.C.P (II)":             {'[columna_omitir]'},
}

# ────────────────────────── 5. PLOT Y ANOTACIONES ─────────────────────────
fig, ax = plot_stacked_bar(
    data_plot, 
    series=componentes,
    title="[TÍTULO DEL GRÁFICO]",
    legend_ncol=3
)

add_hitos_barras(
    ax, data_plot.index, hitos_v_periodos, hitos_offset, hitos_text_x
)

add_cycle_means_barras(
    ax,
    index=list(data_plot.index),   # secuencia de años
    cycle_slices=cycles_adj,       # nombre → slice
    cycle_stats=cycle_stats,       # nombre → {col: media}
    cols=cols,                     # orden de apilado
    offsets=MEAN_OFFSETS_BY_NAME,  # opcional
    skip=SKIP_MEANS_BY_NAME        # opcional
)

# ────────────────────────── 6. GUARDADO ─────────────────────────────
plt.tight_layout()
out_path = OUTPUT_DIR / "[nombre_indicador]_periodos.png"
plt.savefig(out_path, dpi=300, bbox_inches="tight")
plt.show()
plt.close()
```

---

### Reglas del template de barras

| Regla | Detalle |
|---|---|
| **`CYCLES_PERIODOS`** | Es obligatorio usar la variable global `CYCLES_PERIODOS` en vez de versiones sin crisis para gráficas estructurales. |
| **Hitos Verticales** | Utilizar `hitos_v_periodos`, ajustando los años clave (`1952`, `1985`, `2006`, `2015`). |
| **`add_hitos_barras`** | La función especializada para dibujar las líneas sobre las barras apiladas. |
| **`add_cycle_means_barras`** | Usarla para mostrar los valores promedio y las líneas horizontales sobre cada componente en un ciclo económico. |
| **`MEAN_OFFSETS_BY_NAME`** | Debe ajustarse empíricamente con los offsets `(x_offset, y_offset)` requeridos para que los promedios numéricos no colisionen con las barras. |
| **Directorio `ASSETS_DIR`** | Se debe utilizar para estandarizar el guardado de los outputs de la misma forma que en gráficas de líneas. |
