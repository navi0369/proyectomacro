# Skills de Notebooks — Proyectomacro

Este archivo registra los skills disponibles para manipular notebooks `.ipynb` del proyecto.

---

## Skill: `grafica_periodos`

**Propósito:** Modificar (o crear) un notebook para que contenga **exactamente una sola celda de código** que genere únicamente la gráfica de **períodos estructurales** (`_periodos`), usando las constantes `CYCLES_PERIODOS`, `hitos_v_periodos`, `annot_years_periodos` y `periodos_tasas_periodos` del `config.py` global.

---

### Cuándo usarlo

- Cuando el usuario pide generar solo la gráfica de períodos de un indicador.
- Cuando el notebook tiene más gráficas y hay que dejarlo con una sola: la de períodos.
- Cuando hay que crear el notebook desde cero para un indicador nuevo.

---

### Procedimiento obligatorio

1. **Abrir / verificar el notebook** con `mcp_antigravity-nb_open_notebook`.
2. **Listar todas las celdas** con `mcp_antigravity-nb_list_cells`.
3. **Eliminar todas las celdas de código** existentes (de mayor índice a menor para no desplazar índices) con `mcp_antigravity-nb_delete_cell`.
4. **Insertar exactamente una celda de código** en el índice 0 con `mcp_antigravity-nb_insert_cell` siguiendo el template de abajo.
5. **Ejecutar la celda** con `mcp_antigravity-nb_run_cell` para verificar que no hay errores.

> Si el notebook no existe, crearlo primero como archivo `.ipynb` vacío con `run_command` usando el script de creación que aparece al final de este skill.

---

### Template de la celda única

```python
# ═══════════════════════════════════════════════════════════════════
# GRÁFICA DE PERÍODOS ESTRUCTURALES — [NOMBRE_INDICADOR]
# ═══════════════════════════════════════════════════════════════════
import os
import sys
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from func_auxiliares.graficos_utils import (
    set_style,
    init_base_plot,
    add_hitos,
    add_cycle_means_multi,
    add_year_value_annotations,
    add_period_growth_annotations_multi,
    adjust_annot_years,
    adjust_cycles,
    adjust_periods,
    add_period_backgrounds,
)

from func_auxiliares.config import (
    DB_PATH,
    ASSETS_DIR,
    CYCLES_PERIODOS,
    annot_years_periodos,
    periodos_tasas_periodos,
    hitos_v_periodos,
)

# ─────────────────────── 1. CONFIGURACIÓN GENERAL ───────────────────
output_dir = ASSETS_DIR / "serie_completa" / "[nombre_indicador]"
os.makedirs(output_dir, exist_ok=True)
set_style()

# ─────────────────────────── 2. CARGA DE DATOS ──────────────────────
with sqlite3.connect(str(DB_PATH)) as conn:
    df = (
        pd.read_sql(
            "SELECT * FROM [nombre_tabla]",
            conn,
            index_col="año",
        )
        .sort_index()
    )

# ──────────────── 3. COMPONENTES, COLORES Y ABREVIATURAS ────────────
componentes = [
    ("[columna]", "[Etiqueta]"),
    # agregar más si la serie tiene múltiples componentes
]
cols_componentes = [col for col, _ in componentes]

colors = {
    "[columna]": "[color]",
}

abbr_map = {
    "[columna]": "[abr]",
}

# ──────────────── 4. PREPARACIÓN DE CICLOS Y PERÍODOS ───────────────
annotate_years = adjust_annot_years(df, annot_years_periodos)
cycles         = adjust_cycles(df, CYCLES_PERIODOS)
periods        = adjust_periods(df, periodos_tasas_periodos)

cycle_stats = {
    name: df.loc[period, cols_componentes].mean().to_dict()
    for name, period in cycles.items()
}

# ───────────────────── 5. OFFSETS DE POSICIONAMIENTO ────────────────
# Ajustar los valores (x_offset, y_offset) según la escala de la serie

hitos_offset_periodos = {year: 0.8 for year in hitos_v_periodos}

# Anotaciones de valores en años clave
annotation_offsets = {
    "[columna]": {
        1952: (0,  0),   # ← ajustar
        1985: (0,  0),
        2006: (0,  0),
        2014: (0,  0),
        2022: (0,  0),
    },
}

# Posición de medias por período  (año_centro, altura_relativa 0-1)
medias_offsets = {
    "INTERVENSIONISMO ESTATAL": (1960, 0.83),
    "NEOLIBERALISMO": (1998,0.83),
    "E.S.C.P (I)":    (2006, 0.83),
    "E.S.C.P (II)":    (2015, 0.83),
}


# Posición de tasas de crecimiento  (año_centro, altura_relativa 0-1)
tasas_offsets = {
    "1952-1984": (1960, 0.63),
    "1985-2005": (1998, 0.69),
    "2006-2014": (2006, 0.69),
    "2015-2024": (2015, 0.69),
}

# ────────────────────────── 6. GRÁFICO BASE ─────────────────────────
fig, ax = init_base_plot(
    df=df,
    series=componentes,
    colors=colors,
    title=f"[TÍTULO DEL GRÁFICO] ({df.index.min()}–{df.index.max()}) — Períodos Económicos",
    xlabel="Año",
    ylabel="[Unidad de medida]",
    source_text="Fuente: [Fuente de datos]",
)

# ──────────────────── 7. ELEMENTOS GRÁFICOS ─────────────────────────
add_hitos(
    ax, 
    df.index, 
    hitos_v_periodos, 
    hitos_offset_periodos, 
    line_kwargs={"lw": 0.9})

add_cycle_means_multi(
    ax, cycle_stats, medias_offsets,
    abbr_map, colors,
    line_spacing=ax.get_ylim()[1] * 0.03,
)

add_year_value_annotations(
    ax, df, annotate_years,
    cols_componentes, annotation_offsets, colors,
    arrow_lw=0.5,
)

add_period_growth_annotations_multi(
    ax, df, periods,
    cols_componentes, tasas_offsets,
    colors, abbr_map,
)
add_period_backgrounds(
    ax,
    periods,
)

# ────────────────────────── 8. GUARDADO ─────────────────────────────
plt.tight_layout()
fig.savefig(output_dir / "[nombre_indicador]_periodos.png", dpi=300, bbox_inches="tight")
plt.show()
plt.close()
```

---

### Constantes de referencia (`func_auxiliares/config.py`)

```python
CYCLES_PERIODOS= {
    "INTERVENSIONISMO ESTATAL":   slice(1952, 1984),
    "NEOLIBERALISMO":   slice(1985, 2005),
    "E.S.C.P (I)":   slice(2006, 2014),
    "E.S.C.P (II)":   slice(2015, 2024),
} 
#hitos verticales hitos por periodo
hitos_v_periodos = {
    1952: "INTERVENSIONISMO ESTATAL",
    1985: "NEOLIBERALISMO",
    2006: "E.S.C.P (I)",
    2015: "E.S.C.P (II)"
}
annot_years_periodos = [1952,1985,2006,2015,2022]
#anotaciones de tasas con crisis
periodos_tasas_periodos = [
    (1952, 1984),
    (1985, 2005),
    (2006, 2014),
    (2015, 2022)

] 
```

---

### Reglas del template

| Regla | Detalle |
|---|---|
| **Una sola celda** | El notebook debe quedar con exactamente 1 celda de código. |
| **Solo períodos** | No incluir `CYCLES`, `CYCLES_SIN_CRISIS` ni ninguna otra variante. |
| **Imports desde `func_auxiliares`** | Usar rutas absolutas de paquete, no rutas relativas con `sys.path`. |
| **`output_dir`** | Siempre `ASSETS_DIR / "serie_completa" / "[nombre_indicador]"`. |
| **Nombre de archivo de salida** | Siempre termina en `_periodos.png`. |
| **`plt.close()`** | Obligatorio al final para liberar memoria. |
| **Offsets** | Deben ajustarse a la escala real de la serie; los valores del template son placeholders `(0, 0)`. |

---

### Script para crear un notebook vacío (si no existe)

```python
import json, pathlib

path = pathlib.Path("notebooks/tesis/serie_completa/[carpeta]/[nombre].ipynb")
path.parent.mkdir(parents=True, exist_ok=True)
nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": ".venv", "language": "python", "name": "python3"},
        "language_info": {"name": "python"}
    },
    "cells": []
}
path.write_text(json.dumps(nb, indent=1))
print("Notebook creado:", path)
```

---

### Ejemplo de uso completo

Supón que el usuario pide: *"genera la gráfica de períodos para el PIB"*.

1. Verificar que existe `notebooks/tesis/serie_completa/pib/pib.ipynb`.
2. Listar celdas → si hay más de 1 celda de código, borrarlas todas.
3. Copiar el template, reemplazar:
   - `[nombre_indicador]` → `pib`
   - `[nombre_tabla]` → `pib_real` (buscar en `documentacion_tablas.md`)
   - `[columna]` / `[Etiqueta]` / `[color]` / `[abr]` → valores reales
   - `[TÍTULO]`, `[Unidad de medida]`, `[Fuente]` → texto correcto
   - Offsets → valores apropiados para la escala del PIB
4. Insertar la celda en índice 0.
5. Ejecutar y verificar que no hay errores y que se guarda el `.png`.
