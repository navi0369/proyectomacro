# CLAUDE.md — Dashboard Macroeconómico de Bolivia

Guía de referencia rápida para asistentes de IA que trabajen en este proyecto.  
Contiene arquitectura, convenciones, patrones críticos y notas de gotchas para evitar errores comunes.

---

## 1. Visión General del Proyecto

**Nombre:** `proyecto_macro`  
**Propósito:** Dashboard web interactivo para análisis macroeconómico histórico de Bolivia (1950–2024), combinado con un sistema de notebooks para la generación de gráficas estáticas (PNG) destinadas a una tesis académica.  
**Autor:** Juan  
**Stack:** Python 3.8+, Dash (Plotly), SQLite, Matplotlib, Pandas, Jupytext.

El proyecto tiene **dos capas diferenciadas**:

| Capa | Descripción | Tecnología |
|---|---|---|
| **Dashboard Web** | App interactiva con tablas y gráficos dinámicos | Dash + Plotly + DBC |
| **Análisis de Tesis** | Generación de gráficas estáticas con ciclos económicos, hitos, anotaciones | Jupyter Notebooks + Matplotlib |

---

## 2. Estructura del Proyecto

```
proyectomacro-main/
│
├── run.py                          # Punto de entrada principal del dashboard
├── launch_dashboard.py             # Launcher alternativo (abre navegador automáticamente)
├── setup.py                        # Configuración del paquete Python
├── requirements.txt                # Dependencias del proyecto
├── jupytext.toml                   # Sincronización notebooks ↔ scripts Python
├── .env                            # Variables de entorno (Turso DB)
│
├── src/
│   └── proyectomacro/              # Paquete principal del dashboard Dash
│       ├── app.py                  # App Dash: layout, sidebar, callbacks de autenticación
│       ├── config_loader.py        # Carga pages.yml y tables_metadata.yml (clase ConfigLoader)
│       ├── extract_data.py         # Carga tablas validadas desde SQLite + busca imágenes en assets/
│       ├── page_utils.py           # Fábrica de componentes Dash (headers, tablas, galerías, breadcrumbs)
│       ├── config/
│       │   ├── pages.yml           # Configuración completa de secciones y tablas (fuente de verdad)
│       │   └── tables_metadata.yml # Metadata detallada de columnas por tabla
│       ├── pages/                  # Páginas individuales del dashboard (enrutamiento Dash Pages)
│       │   ├── inicio.py
│       │   ├── calculadora.py      # Calculadora interactiva con datos de la BD
│       │   ├── plotter_matplotlib.py  # Generador de gráficas en el dashboard
│       │   ├── cuentas_nacionales/
│       │   ├── sector_externo/
│       │   ├── exportaciones/
│       │   ├── importaciones/
│       │   ├── precios_y_produccion/
│       │   ├── sector_fiscal/
│       │   ├── deuda/
│       │   ├── empleo/
│       │   ├── pobreza/
│       │   └── sector_monetario/
│       └── validation/             # Sistema de validación de datos de la BD
│           ├── rules.yml           # Reglas de validación por tabla
│           ├── validators.py       # Lógica de validación
│           └── validate_all.py     # Ejecuta todas las validaciones
│
├── func_auxiliares/                # Paquete compartido: utils para notebooks Y dashboard
│   ├── config.py                   # PROJECT_ROOT, DB_PATH, ASSETS_DIR + constantes de ciclos económicos
│   └── graficos_utils.py           # Funciones de graficación Matplotlib (versión estable)
│
├── notebooks/
│   └── tesis/
│       └── serie_completa/         # Notebooks de graficación de tesis
│           ├── graficos_utils.py   # ⚠️ VERSIÓN ACTIVA y más completa de graficos_utils
│           ├── config.py           # Config local de la carpeta (similar a func_auxiliares/config.py)
│           └── [carpetas por indicador]/  # pib/, inflacion_acumulada/, exportaciones/, etc.
│
├── scripts/
│   └── tesis/
│       └── serie_completa/         # Espejos .py de los notebooks (sincronizados por Jupytext)
│
├── db/
│   ├── proyectomacro.db            # Base de datos SQLite principal
│   └── proyectomacro.sql           # Dump SQL de la base de datos
│
└── assets/
    └── tesis/
        ├── serie_completa/[tabla]/ # PNGs de gráficas de serie completa por tabla
        └── crisis/[tabla]/         # PNGs de gráficas de periodos de crisis por tabla
```

---

## 3. Arquitectura del Dashboard (Dash)
- **Inicio:** `python run.py` o `python launch_dashboard.py` (URL: `http://0.0.0.0:8050`, Contraseña: `macro2024`)
- **Variables .env:** `DASH_DEBUG`, `DASH_HOST`, `PORT`, `TURSO_DATABASE_URL`, `TURSO_AUTH_TOKEN`.
- **Enrutamiento:** Usa `dash.register_page()` y un sidebar generado dinámicamente desde el `page_registry`.
- **Flujo de autenticación:** Pantalla de login protegida. El estado se guarda en un `dcc.Store(id="session-store", storage_type="session")`.

---

## 4. Base de Datos

- **Motor:** SQLite 3 (archivo `db/proyectomacro.db`, ~336 KB)
- **Índice estándar:** Casi todas las tablas usan `año` como índice entero.
- **Ruta en código:** `from func_auxiliares.config import DB_PATH`

### Patrón estándar para leer datos
```python
from func_auxiliares.graficos_utils import get_df
from func_auxiliares.config import DB_PATH

df = get_df(
    sql="SELECT * FROM nombre_tabla",
    conn_str=str(DB_PATH),
    index_col="año",          # columna de índice (default="año")
    rename={"col_vieja": "col_nueva"},    # opcional
    scale={"columna": 1000},              # opcional: multiplicar
    compute_sum={"total": ["col1","col2"]} # opcional: columna suma
)
```

> **⚠️ Importante:** `get_df` en `func_auxiliares/graficos_utils.py` aplica `round(2)` a todos los numéricos. La versión en `notebooks/tesis/serie_completa/graficos_utils.py` NO aplica el redondeo automático (es la versión más activa).

### Validación de datos
```python
from proyectomacro.extract_data import load_validated_tables
# Carga solo las tablas con status "OK" según rules.yml
dfs = load_validated_tables()
```

---

## 5. Sistema de Configuración YAML

### `src/proyectomacro/config/pages.yml`
Fuente de verdad para todas las secciones y tablas del dashboard. Estructura:
```yaml
secciones:
  cuentas_nacionales:
    name: "Cuentas Nacionales"
    tablas:
      pib_ramas:
        tabla: "pib_ramas_actividad"
        label: "PIB por Ramas de Actividad"
        metadata:
          nombre_descriptivo: "..."
          periodo: "1950 – 2022"
          unidad: "Millones de Bs de 1990"
          fuentes: ["INE", "UDAPE"]
          notas: "..."
```

### `src/proyectomacro/config/tables_metadata.yml`
Metadata detallada por columna (tipo, unidad, escala, moneda, año base).

### `func_auxiliares/config.py`
Constantes globales del proyecto:
```python
PROJECT_ROOT  # Raíz del proyecto
DB_PATH       # Ruta a proyectomacro.db
ASSETS_DIR    # assets/tesis/

# Constantes de análisis económico
CYCLES        # Ciclos económicos bolivianos (1952-2024) → dict[str, slice]
CYCLES_SIN_CRISIS  # Ciclos sin periodos de crisis
CYCLES_PERIODOS    # Ciclos por modelo económico (Intervensionismo, Neoliberalismo, ESCP)
hitos_v            # Hitos verticales: {año: etiqueta}
periodos_tasas     # Lista de tuplas (ini, fin) para tasas de crecimiento
```

---

## 6. Graficación con Matplotlib (Notebooks de Tesis)

### ⚠️ Dos versiones de `graficos_utils.py`

| Archivo | Uso | Diferencias clave |
|---|---|---|
| `func_auxiliares/graficos_utils.py` | Dashboard + notebooks legacy | `init_base_plot` sin param `color`/`fontsize`, redondeo en `get_df` |
| `notebooks/tesis/serie_completa/graficos_utils.py` | **Notebooks activos de tesis** | Más funciones (`add_period_backgrounds`, `init_dual_axis_plot`), `init_base_plot` con params `color` y `fontsize` |

**Usar siempre la versión de notebooks cuando se trabaja en análisis de tesis.**

### Flujo estándar en un notebook de tesis
```python
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # o ajustar
from graficos_utils import (
    get_df, set_style, init_base_plot,
    add_hitos, add_period_backgrounds,
    adjust_cycles, adjust_periods, adjust_annot_years,
    add_period_growth_annotations_multi, add_cycle_means_multi
)
from config import (DB_PATH, ASSETS_DIR, CYCLES, hitos_v, periodos_tasas, annot_years)

# 1. Cargar y preparar datos
df = get_df("SELECT * FROM tabla", conn_str=str(DB_PATH))

# 2. Ajustar ciclos al rango real del df
cycles_adj = adjust_cycles(df, CYCLES)

# 3. Configurar estilo global
set_style()

# 4. Crear figura base
fig, ax = init_base_plot(
    df, series=[("col","Etiqueta")], colors={"col":"#1f77b4"},
    title="Título", xlabel="Año", ylabel="Unidad",
    source_text="Fuente: UDAPE/INE"
)

# 5. Añadir elementos decorativos
add_period_backgrounds(ax, ...)  # fondos de color por ciclo
add_hitos(ax, df.index, hitos_v, ...)  # líneas verticales de hitos

# 6. Guardar
fig.savefig(ASSETS_DIR / "serie_completa" / "tabla" / "grafica.png")
```

### Funciones principales de `graficos_utils.py`

| Función | Propósito |
|---|---|
| `get_df(sql, conn_str, ...)` | Leer de SQLite con transformaciones opcionales |
| `set_style()` | Aplica estilo seaborn-whitegrid + fuente serif, dpi=150 |
| `init_base_plot(df, series, colors, ...)` | Crea fig/ax con líneas, leyenda, título, pie de fuente |
| `init_dual_axis_plot(...)` | Gráfico de dos ejes Y (solo en versión notebooks) |
| `plot_stacked_bar(data, series, ...)` | Barras apiladas con leyenda inferior |
| `add_period_backgrounds(ax, periods, colors, ...)` | Fondos coloreados por periodo histórico |
| `add_hitos(ax, index, hitos_v, hitos_offset, ...)` | Líneas verticales + etiquetas de hitos |
| `add_hitos_barras(ax, index, hitos_v, ...)` | Hitos sobre gráficos de barras (posición en índice) |
| `add_period_growth_annotations_multi(...)` | Anotaciones de tasas de crecimiento por periodo |
| `add_cycle_means_multi(...)` | Anotaciones de medias por ciclo y componente |
| `add_year_value_annotations(...)` | Flechas + valores sobre puntos específicos |
| `adjust_cycles(df, cycles)` | Ajusta slices al rango real del DataFrame |
| `adjust_periods(df, periods, ...)` | Ajusta tuplas (ini,fin) al rango real + extiende último |
| `adjust_annot_years(df, years)` | Filtra años de anotación al rango del DataFrame |
| `update_periods(original, rename_map, add_list)` | Modifica lista de periodos idempotentemente |
| `update_dict(original, rename_map, ...)` | Modifica dict de ciclos idempotentemente |

### Patrón `add_hitos` — VERSIÓN NOTEBOOKS (la correcta)
La versión de `notebooks/tesis/serie_completa/graficos_utils.py` acepta `periodos_texto` para centrar el texto del hito en el **promedio del periodo** (no en el año exacto):
```python
add_hitos(
    ax, df.index, hitos_v, hitos_offset,
    periodos_texto={
        1952: (1952, 1984),  # texto centrado en (1952+1984)/2
        1985: (1985, 2005),
    },
    annotate_labels=('Crisis', 'Expansión', 'Recesión', 'Transición'),
)
```

---

## 7. Componentes Reutilizables del Dashboard (`page_utils.py`)

Las páginas del dashboard usan componentes predefinidos en `src/proyectomacro/page_utils.py`:
- `build_header()`: Título + metadata colapsable
- `build_breadcrumb()`: Fila breadcrumb + badge de estado
- `build_data_table()`: DataTable estándar
- `build_image_gallery_card()`: Card con tabs de imágenes

**Patrón básico de página:**
Carga de datos → `dfs.get(TABLE_ID)`, metadatos → `load_metadata_from_config(TABLE_ID)`, e imágenes → `list_table_image_groups(TABLE_ID)`, luego se renderizan usando las funciones `build_*`.

---

## 8. Jupytext — Sincronización Notebooks ↔ Scripts

Configurado en `jupytext.toml`:
```toml
formats = "notebooks///ipynb,scripts///py:percent"
```

- Los notebooks en `notebooks/` tienen su espejo `.py` en `scripts/` (formato `percent`).
- Al editar el `.ipynb` y guardarlo, Jupytext actualiza el `.py` automáticamente.
- Para sincronizar manualmente: `jupytext --sync notebooks/tesis/serie_completa/*.ipynb`

---

## 9. Instalación y Desarrollo

```bash
# Clonar y entrar al proyecto
cd proyectomacro-main

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Instalar paquete en modo desarrollo (importante: permite imports de func_auxiliares)
pip install -e .

# Ejecutar el dashboard
python run.py
```

### Imports críticos y rutas de Python
El proyecto manipula `sys.path` explícitamente en `run.py`:
```python
sys.path.insert(0, current_dir)       # raíz del proyecto
sys.path.insert(0, os.path.join(current_dir, 'src'))  # src/
```

En los notebooks, usar `PYTHONPATH` o ajustar manualmente:
```python
import sys
from pathlib import Path
# Apuntar a la raíz del proyecto
sys.path.insert(0, str(Path(__file__).resolve().parents[N]))
```

---

## 10. Ciclos Económicos de Bolivia (Constantes)

Definidos en `func_auxiliares/config.py`:

```python
CYCLES = {
    "Crisis 52-55":      slice(1952, 1955),
    "Expansión 56-69":   slice(1956, 1969),
    "Recesión 70-81":    slice(1970, 1981),
    "Crisis 82-84":      slice(1982, 1984),
    "Expansión 85-00":   slice(1985, 2000),
    "Transicion 01-05":  slice(2001, 2005),
    "Expansión 06-14":   slice(2006, 2014),
    "Recesión 15-24":    slice(2015, 2024),
}

# Hitos verticales en las gráficas
hitos_v = {
    1952: "Crisis", 1956: "Expansión", 1970: "Recesión",
    1982: "Crisis", 1985: "Expansión", 2001: "Transición",
    2006: "Expansión", 2014: "Recesión"
}

# Modelos económicos de Bolivia
CYCLES_PERIODOS = {
    "Intervensionismo-estatal 52-84": slice(1952, 1984),
    "Neoliberalismo 85-05":           slice(1985, 2005),
    "E.S.C.P (I)":                    slice(2006, 2014),
    "E.S.C.P (II)":                   slice(2015, 2024),
}
```

---

## 11. Gotchas y Patrones Importantes

### ⚠️ Dos `graficos_utils.py` diferentes
- **`func_auxiliares/graficos_utils.py`** → usada por el dashboard y notebooks legacy.
- **`notebooks/tesis/serie_completa/graficos_utils.py`** → versión activa y más completa para tesis. Tiene funciones adicionales como `add_period_backgrounds` e `init_dual_axis_plot`. El `init_base_plot` aquí acepta los parámetros `color` y `fontsize` que la versión de `func_auxiliares` NO tiene.

### ⚠️ No editar archivos `.ipynb` directamente
Los archivos `.ipynb` solo se pueden modificar mediante:
1. La interfaz de Jupyter Lab/Notebook.
2. Scripts Python que manipulen el JSON con `json.load/dump`.
3. Las herramientas MCP `antigravity-nb` si están disponibles.

### ⚠️ `adjust_cycles` es obligatorio antes de usar ciclos
Siempre ajustar los slices al rango real del DataFrame:
```python
cycles_adj = adjust_cycles(df, CYCLES)  # NO usar CYCLES directamente
```

### ⚠️ `page_utils.build_data_table` modifica `table_styles` in-place
Llama a `table_styles.pop("style_data_conditional", [])`. Si se reutiliza el dict de estilos, pasarlo como copia.

### ⚠️ Matplotlib backend en el dashboard
En `plotter_matplotlib.py`, se usa `matplotlib.use('Agg')` para renderizado sin pantalla. Las gráficas se convierten a base64 PNG para mostrarlas en Dash.

### ⚠️ `load_validated_tables` es costoso
Ejecuta validación completa de la BD. En producción se llama una vez al iniciar la página, no por cada interacción.

### ⚠️ IDs de componentes Dash deben ser únicos globalmente
Con `suppress_callback_exceptions=True`, los errores de IDs duplicados pueden pasar silenciosamente. Al añadir páginas nuevas, verificar que los IDs no colisionen.

---

## 12. Herramientas MCP Disponibles (`antigravity-nb`)

Para trabajar con notebooks Jupyter desde el asistente de IA:

| Herramienta | Acción |
|---|---|
| `mcp_antigravity-nb_open_notebook` | Abre un notebook y retorna metadatos |
| `mcp_antigravity-nb_list_cells` | Lista todas las celdas con índice y preview |
| `mcp_antigravity-nb_read_cell` | Lee código, outputs y metadata de una celda |
| `mcp_antigravity-nb_insert_cell` | Inserta nueva celda en un índice |
| `mcp_antigravity-nb_edit_cell` | Modifica el código fuente de una celda |
| `mcp_antigravity-nb_delete_cell` | Elimina una celda |
| `mcp_antigravity-nb_run_cell` | Ejecuta una celda y retorna outputs |
| `mcp_antigravity-nb_run_range` | Ejecuta rango de celdas [start, end] |
| `mcp_antigravity-nb_run_pipeline` | Ejecuta celdas agrupadas por pipeline tags |
| `mcp_antigravity-nb_restart_kernel` | Reinicia el kernel del notebook |

> **Nota:** Las herramientas MCP de notebooks solo funcionan con rutas relativas al workspace configurado. Si fallan con "path outside workspace", usar `run_command` con `jupyter nbconvert` o scripts Python para manipular el JSON.

---

## 13. Archivos de Documentación Existentes

| Archivo | Contenido |
|---|---|
| `DOCUMENTACION_PLOTTER_MATPLOTLIB.md` | Documentación detallada del módulo plotter |
| `Guia_Graficas_Serie_Completa.md` | Guía de gráficas de línea para tesis |
| `Guia_Graficas_Barplot_Serie_Completa.md` | Guía de gráficas de barras para tesis |
| `TABLE_STYLES_SYSTEM.md` | Sistema de estilos para tablas Dash |
| `METADATA_SYSTEM.md` | Sistema de metadata YAML |
| `documentacion_tablas.md` | Documentación de todas las tablas de la BD |
| `readme_db.md` | Documentación de la base de datos |
| `readme_jupytext.md` | Guía de uso de Jupytext en el proyecto |
| `docs/generador_graficas.md` | Documentación del generador de gráficas |
| `docs/cambios_plotter_init_base_plot.md` | Cambios en `init_base_plot` |

---

## 14. Skills Disponibles (`skills/`)

El directorio `skills/` contiene comportamientos y plantillas que encapsulan tareas rutinarias.

| Skill / Directorio | Descripción |
|---|---|
| `SKILL.md` (grafica_periodos) | Instrucciones detalladas para modificar notebooks de manera que generen exclusivamente la gráfica de *períodos estructurales* usando constantes como `CYCLES_PERIODOS`. |
| `estandarizar_graficas/` | Directorio diseñado para agrupar los skills y automatizaciones relacionadas a la estandarización de gráficas de la tesis. |
