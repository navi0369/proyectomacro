# Skills de Notebooks — Proyectomacro (Gráficas de Doble Eje / Eje Dual)

Este archivo registra los skills disponibles para manipular y estandarizar notebooks `.ipynb` que contienen **gráficas de doble eje (eje dual)** (ej. Valor/Volumen en el eje izquierdo y Precio en el eje derecho).

---

## Skill: `grafica_periodos_doble_eje`

**Propósito:** Modificar o crear celdas de código en un notebook `.ipynb` enfocadas en generar gráficas de **períodos estructurales en eje dual**, usando las constantes globales de `config.py` (`CYCLES_PERIODOS`, `hitos_v_periodos`, `annot_years_periodos`, `periodos_tasas_periodos`) y las funciones específicas de doble eje de `graficos_utils.py` (`init_dual_axis_plot`, `add_hitos`, `add_cycle_means_multi`, `add_year_value_annotations`, `add_period_growth_annotations_multi`, `adjust_annot_years`, `adjust_cycles`, `adjust_periods`).

---

### Cuándo usarlo

- Cuando el usuario pide graficar o estandarizar un indicador que tiene dos unidades de medida distintas (ej. Volumen en toneladas/kilogramos vs. Precio en USD por onza/tonelada, o Valor en millones de USD vs. Precio en USD).
- Cuando el notebook requiere representar la evolución histórica de dos series correlacionadas pero en escalas sumamente diferentes mediante ejes Y izquierdo y derecho (Dual Axis).

---

### Procedimiento obligatorio

1. **Abrir / verificar el notebook** con las herramientas MCP disponibles.
2. **Listar las celdas** para identificar la lógica previa de extracción SQL.
3. **Analizar la lógica previa de transformación de datos** (cargas de tablas de exportación y precio, uniones `.join()`, conversiones de unidades como dividir por 1,000 para pasar de miles a millones de USD, etc.) y **mantenerla**.
4. **Reemplazar o editar las celdas del notebook** para incorporar los templates de eje dual estandarizados mostrados abajo.
5. **Ejecutar las celdas** para verificar la correcta generación de las imágenes `.png` en los directorios de destino en `assets/`.

---

### Templates de las celdas

Para las series de minerales que requieren visualizar **Valor vs. Precio** y **Volumen vs. Precio**, el notebook típicamente se estructurará en dos celdas principales de graficación, además del preprocesamiento.

#### Celda 1: Preparación de Datos y Gráfica de Valor vs. Precio

```python
# ═══════════════════════════════════════════════════════════════════
# PREPARACIÓN Y GRÁFICA DE VALOR VS. PRECIO (DOBLE EJE) — [NOMBRE_MINERAL]
# ═══════════════════════════════════════════════════════════════════
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from func_auxiliares.graficos_utils import (
    set_style,
    init_dual_axis_plot,
    add_hitos,
    add_cycle_means_multi,
    add_year_value_annotations,
    add_period_growth_annotations_multi,
    adjust_annot_years,
    adjust_cycles,
    adjust_periods,
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
# Definir los directorios de salida usando ASSETS_DIR
output_dir = ASSETS_DIR / "serie_completa" / "[carpeta_exportaciones]"
os.makedirs(output_dir, exist_ok=True)

output_dir_precio = ASSETS_DIR / "serie_completa" / "[carpeta_precios]"
os.makedirs(output_dir_precio, exist_ok=True)

set_style()

# ─────────────────────────── 2. CARGA DE DATOS ──────────────────────
# Cargar datos de exportaciones y precios oficiales de la base de datos
with sqlite3.connect(str(DB_PATH)) as conn:
    df_export = (
        pd.read_sql(
            "SELECT año, [columna_volumen], [columna_valor] FROM exportaciones_minerales_totales", 
            conn
        )
        .set_index("año")
        .sort_index()
    )
    df_precio = (
        pd.read_sql(
            "SELECT año, [columna_precio_tabla] AS precio_usd_ot FROM precio_oficial_minerales", 
            conn
        )
        .set_index("año")
        .sort_index()
    )

# Unir y realizar transformaciones (ej. convertir valor de miles a millones de USD si aplica)
df = df_export.join(df_precio, how="inner")
df["[nombre_columna_valor_transformada]"] = df["[columna_valor]"] / 1_000   # miles → millones
df.drop(columns="[columna_valor]", inplace=True)

# ──────────────── 3. COMPONENTES, COLORES Y ABREVIATURAS ────────────
cols = ["[nombre_columna_valor_transformada]", "precio_usd_ot"]
abbr = {
    "[nombre_columna_valor_transformada]": "Valor", 
    "precio_usd_ot": "Precio"
}
colors = {
    "[nombre_columna_valor_transformada]": "#1f77b4", 
    "precio_usd_ot": "red"
}

# ──────────────── 4. PREPARACIÓN DE CICLOS Y PERÍODOS ───────────────
CYCLES = adjust_cycles(df, CYCLES_PERIODOS)
cycle_stats = {n: df.loc[s, cols].mean().to_dict() for n, s in CYCLES.items()}

hitos_offset = {yr: .60 for yr in hitos_v_periodos}
anot_years = adjust_annot_years(df, annot_years_periodos)
growth_periods = adjust_periods(df, periodos_tasas_periodos)

# ───────────────────── 5. OFFSETS DE POSICIONAMIENTO ────────────────
# ⚠️ Ajustar empíricamente para evitar solapamientos visuales según la escala de la serie
annotation_offsets = {
    "[nombre_columna_valor_transformada]": {
        1952: (0, 25),
        1985: (0, 36),
        2006: (-0.7, 45),
        2015: (0, 30),
        2022: (0, 30),
    },
    "precio_usd_ot": {
        1952: (0, -0.9),
        1985: (-0.7, -0.8),
        2006: (-1.3, 1),
        2015: (0, -1),
        2022: (1.9, 0),
    },
}

period_growth_offsets = {
    "1952-1984": (1960, 0.78),
    "1985-2005": (1991, 0.78),
    "2006-2014": (2008.2, 0.1),
    "2015-2024": (2016, 0.82),
}

cycle_text_offsets = {
    "INTERVENSIONISMO ESTATAL": (1960, 0.92),
    "NEOLIBERALISMO":          (1991, 0.92),
    "E.S.C.P (I)":             (2008.2, 0.22),
    "E.S.C.P (II)":            (2016, 0.95),
}

# ─────────────────── 6. PLOT Y ANOTACIONES DUAL AXIS ───────────────────
left_series  = [("[nombre_columna_valor_transformada]", "Valor exportado (M USD)")]
right_series = [("precio_usd_ot", "Precio (USD/[unidad_precio])")]

fig, ax_val, ax_price = init_dual_axis_plot(
    df=df,
    left_series=left_series,
    right_series=right_series,
    colors=colors,
    title=f"[NOMBRE_INDICADOR_MAYUSCULAS] VALOR VS. PRECIO ({df.index[0]}–{df.index[-1]})",
    xlabel="Año",
    left_ylabel="Valor exportado (millones USD)",
    right_ylabel="Precio (USD por [unidad_precio])",
    source_text="Fuente: Elaboración propia con datos de Memorias del banco central y Ministerio de minería y metalurgia"
)

# Agregar hitos, promedios de ciclos, etiquetas de años y tasas de crecimiento
add_hitos(ax_val, df.index, hitos_v_periodos, hitos_offset, line_kwargs={"lw":1})

add_cycle_means_multi(
    ax_val, cycle_stats, cycle_text_offsets,
    abbr, colors, line_spacing=df["[nombre_columna_valor_transformada]"].max()*0.03,
    value_fmt="{:,.1f}"
)

add_year_value_annotations(
    ax_val, df, anot_years, ["[nombre_columna_valor_transformada]"],
    {"[nombre_columna_valor_transformada]": annotation_offsets["[nombre_columna_valor_transformada]"]},
    {"[nombre_columna_valor_transformada]": colors["[nombre_columna_valor_transformada]"]}, arrow_lw=0.6
)

add_year_value_annotations(
    ax_price, df, anot_years, ["precio_usd_ot"],
    {"precio_usd_ot": annotation_offsets["precio_usd_ot"]},
    {"precio_usd_ot": colors["precio_usd_ot"]}, arrow_lw=0.6,
    value_fmt="{:,.1f}"
)

add_period_growth_annotations_multi(
    ax_val, df, growth_periods, cols,
    period_growth_offsets, colors, abbr
)

# Ajuste de Leyenda Combinada
h, l   = ax_val.get_legend_handles_labels()
h2, l2 = ax_price.get_legend_handles_labels()
hl    = [(x, y) for x, y in zip(h + h2, l + l2) if not y.startswith('_')]
if hl: 
    ax_val.legend(*zip(*hl), loc="upper left", fontsize=11)

# Guardar Gráficas
plt.tight_layout()
plt.savefig(output_dir / "[nombre_mineral]_valor_precio_dual_axis.png", dpi=300)
plt.savefig(output_dir_precio / "[nombre_mineral]_precio_dual_axis.png", dpi=300)
plt.show()
plt.close()
```

#### Celda 2: Gráfica de Volumen vs. Precio

```python
# ═══════════════════════════════════════════════════════════════════
# GRÁFICA DE VOLUMEN VS. PRECIO (DOBLE EJE) — [NOMBRE_MINERAL]
# ═══════════════════════════════════════════════════════════════════

# ──────────────── 1. COMPONENTES, COLORES Y ABREVIATURAS ────────────
cols_vol   = ["[columna_volumen]", "precio_usd_ot"]
colors_vol = {
    "[columna_volumen]": "#1f77b4",
    "precio_usd_ot": colors["precio_usd_ot"]
}
abbr_vol = {
    "[columna_volumen]": "Vol", 
    "precio_usd_ot": "P"
}

cycle_stats_vol = {n: df.loc[s, cols_vol].mean().to_dict() for n, s in CYCLES.items()}

# ───────────────────── 2. OFFSETS DE POSICIONAMIENTO ────────────────
# ⚠️ Ajustar empíricamente para evitar solapamientos visuales según la escala de la serie
annotation_offsets_vol = {
    "[columna_volumen]": {
        1952: (0, 25),
        1985: (0, -35),
        2006: (1.3, -35),
        2015: (0, 15),
        2022: (0, 15),
    },
    "precio_usd_ot": {
        1952: (0, -0.8),
        1985: (0, -1.2),
        2006: (-0.5, 2.2),
        2015: (0, -1),
        2022: (0.55, 1),
    },
}

period_growth_offsets_vol = {
    "1952-1984": (1960, 0.78),
    "1985-2005": (1991, 0.78),
    "2006-2014": (2006.2, 0.1),
    "2015-2024": (2017, 0.1),
}

cycle_text_offsets_vol = {
    "INTERVENSIONISMO ESTATAL": (1960, 0.92),
    "NEOLIBERALISMO":          (1991, 0.92),
    "E.S.C.P (I)":             (2006.2, 0.22),
    "E.S.C.P (II)":            (2017, 0.22),
}

# ─────────────────── 3. PLOT Y ANOTACIONES DUAL AXIS ───────────────────
left_series_vol  = [("[columna_volumen]", "Volumen ([unidad_volumen])")]
right_series_vol = [("precio_usd_ot", "Precio (USD/[unidad_precio])")]

fig_v, ax_v, ax_price_v = init_dual_axis_plot(
    df=df,
    left_series=left_series_vol,
    right_series=right_series_vol,
    colors=colors_vol,
    title=f"[NOMBRE_INDICADOR_MAYUSCULAS] VOLUMEN VS. PRECIO ({df.index[0]}–{df.index[-1]})",
    xlabel="Año",
    left_ylabel="Volumen ([unidad_volumen])",
    right_ylabel="Precio (USD por [unidad_precio])",
    source_text="Fuente: Elaboración propia con datos de Memorias del banco central y Ministerio de minería y metalurgia"
)

# Trazar Hitos y Líneas
add_hitos(ax_v, df.index, hitos_v_periodos, hitos_offset, line_kwargs={"lw":1})

# Espaciado vertical relativo para las medias
y_min, y_max = ax_v.get_ylim()
line_spacing = (y_max - y_min) * 0.03

# Medias por ciclo
add_cycle_means_multi(
    ax_v, cycle_stats_vol, cycle_text_offsets_vol,
    abbr_vol, colors_vol, line_spacing=line_spacing,
    value_fmt="{:,.1f}"
)

# Anotaciones de valor anual
add_year_value_annotations(
    ax_v, df, anot_years, ["[columna_volumen]"],
    {"[columna_volumen]": annotation_offsets_vol["[columna_volumen]"]},
    {"[columna_volumen]": colors_vol["[columna_volumen]"]}, arrow_lw=0.6
)
add_year_value_annotations(
    ax_price_v, df, anot_years, ["precio_usd_ot"],
    {"precio_usd_ot": annotation_offsets_vol["precio_usd_ot"]},
    {"precio_usd_ot": colors_vol["precio_usd_ot"]}, arrow_lw=0.6,
    value_fmt="{:,.1f}"
)

# Tasas de crecimiento por periodo
add_period_growth_annotations_multi(
    ax_v, df, growth_periods, cols_vol,
    period_growth_offsets_vol, colors_vol, abbr_vol,
    line_spacing_ratio=0.03
)

# Ajuste de Leyenda
h1, l1 = ax_v.get_legend_handles_labels()
h2, l2 = ax_price_v.get_legend_handles_labels()
ax_v.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=11)

# Guardar Gráfica de Volumen
plt.tight_layout()
plt.savefig(output_dir / "[nombre_mineral]_volumen_precio_dual_axis.png", dpi=300)
plt.savefig(output_dir_precio / "[nombre_mineral]_precio_dual_axis.png", dpi=300)
plt.show()
plt.close()
```

---

### Reglas del template de eje dual

| Regla | Detalle |
|---|---|
| **Eje Dual Coherente** | El eje Y izquierdo (`ax_left`) siempre debe mostrar el Valor o Volumen, y el eje Y derecho (`ax_right`) el Precio, para mantener consistencia visual. |
| **`CYCLES_PERIODOS`** | Es obligatorio usar la variable global `CYCLES_PERIODOS` para gráficas de períodos estructurales. |
| **Hitos Verticales** | Utilizar `hitos_v_periodos`, dibujados por `add_hitos` en el eje izquierdo para evitar duplicaciones visuales. |
| **`init_dual_axis_plot`** | Utilidad indispensable para instanciar correctamente la figura de dos ejes Y (`ax_left` y `ax_right`) con sus respectivos títulos y colores coordinados. |
| **Gestión de Leyendas** | Es crítico unir los handles y labels de ambos ejes (`ax_val` y `ax_price`) en una sola llamada de leyenda en `ax_val` para que figuren todas las series representadas. |
| **Directorio `ASSETS_DIR`** | Se debe utilizar para estandarizar el guardado de los outputs (`ASSETS_DIR / "serie_completa" / ...`) en lugar de rutas relativas con `../`. |
| **`plt.close()`** | Es obligatorio cerrar explícitamente cada figura al final de la celda mediante `plt.close()` para liberar memoria gráfica del kernel. |
| **Ajuste de Offsets** | Los diccionarios de offsets de anotación y tasas deben calibrarse manualmente por cada indicador según el rango de valores de su eje izquierdo para que no se superpongan los textos de medias o tasas. |
