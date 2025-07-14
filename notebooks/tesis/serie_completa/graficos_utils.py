import pandas as pd
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Sequence, Mapping, Set
import logging
import numpy as np
logger = logging.getLogger(__name__)
# graficos_utils.py


from typing import List, Tuple, Dict

Period = Tuple[int, int]

def update_periods(
    original: List[Period],
    rename_map: Dict[Period, Period] = {},
    add_list:    List[Period]       = []
) -> List[Period]:
    """
    Idempotentemente:
      1) Reemplaza cada tupla que aparezca en rename_map (old→new).
      2) Añade al final las tuplas de add_list que no estuvieran ya.
    No mutate la lista original; retorna una copia.
    """
    # 1) Aplico renombrados/reemplazos
    updated = [ rename_map.get(p, p) for p in original ]
    
    # 2) Agrego nuevas tuplas si no existen
    for p in add_list:
        if p not in updated:
            updated.append(p)
    
    return updated


def update_dict(
    original: dict[str, slice],
    rename_map: dict[str, str] = {},
    rename_values: dict[str, slice] = {},
    add_map:    dict[str, slice] = {}
) -> dict[str, slice]:
    """
    Idempotentemente:
      1) Renombra claves según rename_map,
         y si rename_values[new_key] existe, usa ese slice en lugar del original.
      2) Añade nuevos pares clave→slice de add_map.
    """
    out = original.copy()

    # 1) Renombrar (y opcionalmente cambiar valor)
    for old_key, new_key in rename_map.items():
        if old_key in out and new_key not in out:
            # Extraigo el slice antiguo...
            val = out.pop(old_key)
            # ...pero si hay override en rename_values, lo uso:
            val = rename_values.get(new_key, val)
            out[new_key] = val

    # 2) Añadir nuevos periodos
    for key, sl in add_map.items():
        if key not in out:
            out[key] = sl

    return out



def add_cycle_means_barras(
    ax: plt.Axes,
    index: Sequence[int],
    cycle_slices: Mapping[str, slice],
    cycle_stats: Mapping[str, Dict[str, float]],
    cols: Sequence[str],
    *,
    offsets: Mapping[str, Dict[str, Tuple[float, float]]] | None = None,
    skip:    Mapping[str, Set[str]] | None = None,
    bar_width: float = 0.8,
    fmt: str = "{val:.0f}",
    text_kwargs: Dict | None = None
) -> None:
    """
    Anota los promedios de `cycle_stats` sobre un gráfico de barras apiladas.

    Parameters
    ----------
    ax : plt.Axes
        El eje donde dibujar.
    index : Sequence[int]
        Índice de años (df.index.values).
    cycle_slices : {nombre_ciclo: slice}
        Permite calcular la posición horizontal (centro del ciclo).
    cycle_stats : {nombre_ciclo: {col: media}}
        Diccionario con las medias ya precalculadas.
    cols : list[str]
        Orden de columnas tal como se dibujaron en el bar-chart.
    offsets : {nombre_ciclo: {col: (dx, dy)}}, opcional
        Desplazamientos específicos por ciclo/columna.
    skip : {nombre_ciclo: {col1, col2}}, opcional
        Conjunto de columnas que NO se quieren anotar.
    bar_width : float
        Para centrar correctamente en la barra.
    fmt : str
        Formato de texto para la media.
    text_kwargs : dict, opcional
        kwargs adicionales para `ax.text`.
    """
    if text_kwargs is None:
        text_kwargs = {
            'fontsize': 13,
            'color': 'black',
            'ha': 'center',
            'va': 'center',
            'fontweight': 'bold',
            'zorder': 6
        }

    for name, stats in cycle_stats.items():
        if name not in cycle_slices:
            # Estadística sin slice correspondiente → ignoro
            continue

        sl = cycle_slices[name]
        # ---------------- coordenada X (centro del ciclo) ------------------
        start_idx = index.index(sl.start)
        end_idx   = index.index(sl.stop)
        x_mid     = (start_idx + end_idx) / 2 + bar_width / 2        # centro

        # ---------------- iterar columnas en orden de apilado -------------
        cum = 0                                    # acumulado para stacked
        for col in cols:
            if skip and col in skip.get(name, set()):
                cum += stats[col]
                continue

            val = stats[col]
            dx, dy = (0.0, 0.0)
            if offsets:
                dx, dy = offsets.get(name, {}).get(col, (0.0, 0.0))

            ax.text(
                x_mid + dx,
                cum + val/2 + dy,
                fmt.format(val=val),
                transform=ax.transData,
                **text_kwargs
            )
            cum += val
def adjust_cycles(df: pd.DataFrame, cycles: dict[str, slice]) -> dict[str, slice]:
    if df.empty:
        raise ValueError("DF vacío")

    min_year, max_year = map(int, [df.index.min(), df.index.max()])
    # — 1. encontrar el slice con stop más grande —
    last_nominal_stop = max(sl.stop for sl in cycles.values())
    cycles_adj = {}

    for name, sl in cycles.items():
        start = max(sl.start, min_year)

        # — 2. si es el último ciclo, usamos max_year como fin —
        stop_incl = max_year if sl.stop == last_nominal_stop else min(sl.stop, max_year)

        if start <= stop_incl:
            # Pandas .loc es inclusivo, así que usamos stop_incl tal cual
            new_key = name
            if start != sl.start or stop_incl != sl.stop:
                base = name.rsplit(" ", 1)[0]
                new_key = f"{base} {start%100:02d}-{stop_incl%100:02d}"

            cycles_adj[new_key] = slice(start, stop_incl)
        else:
            logger.warning("Ciclo %s ignorado (fuera de rango)", name)

    return cycles_adj

def adjust_periods(
    df: pd.DataFrame,
    periods: List[Tuple[int, int]],
    required_cols: Optional[List[str]] = None,
    min_nonzero: int = 1
) -> List[Tuple[int, int]]:
    """
    Ajusta los períodos nominales a lo que realmente existe en `df`
    y extiende el ÚLTIMO período hasta el máximo año en que TODAS
    las `required_cols` tienen datos válidos (no NaN, ≠0).

    Parámetros
    ----------
    df : DataFrame con índice numérico (años).
    periods : lista [(ini, fin), ...] nominal.
    required_cols : columnas que deben tener datos válidos.
                    Si None, usa todas las columnas numéricas.
    min_nonzero : nº mínimo de valores válidos por período
                  para que éste se conserve.
    """
    if df.empty:
        return []

    if required_cols is None:
        required_cols = [
            c for c in df.columns
            if np.issubdtype(df[c].dtype, np.number)
        ]

    years = df.index.astype(int)
    min_year, max_year = years.min(), years.max()

    # -- helper: cuántos valores válidos hay por periodo
    def valid_count(lo, hi):
        sub = df.loc[lo:hi, required_cols]
        return ((sub.notna()) & (sub != 0)).sum().sum()

    adjusted = []

    for idx, (start, stop) in enumerate(periods):
        lo = max(start, min_year)
        hi = min(stop,  max_year)
        if lo > hi:
            continue

        # recorte al rango real de años disponibles
        available = years[(years >= lo) & (years <= hi)]
        if available.empty:
            continue

        lo2, hi2 = available.min(), available.max()

        # filtro por datos válidos
        if valid_count(lo2, hi2) < min_nonzero:
            continue

        adjusted.append((int(lo2), int(hi2)))

    # ---------------------------
    # Empujar el ÚLTIMO período
    # ---------------------------
    if adjusted:
        # último año donde TODAS las columnas tienen dato válido
        mask_valid = (df[required_cols].notna() & (df[required_cols] != 0)).all(axis=1)
        if mask_valid.any():
            last_valid_year = int(df.index[mask_valid].max())
            # sustituir el 'stop' de la última tupla si podemos crecer
            lo_last, hi_last = adjusted[-1]
            if last_valid_year > hi_last:
                adjusted[-1] = (lo_last, last_valid_year)

    return adjusted
def adjust_annot_years(df: pd.DataFrame, years: List[int]) -> List[int]:
    """
    Filtra y ajusta la lista `years` para que:
      1. Queden solo los años entre el primer y último año de df.index.
      2. El primer elemento sea siempre df.index.min().
      3. El último elemento sea siempre df.index.max().
      4. No haya duplicados, ni viejos valores iguales al máximo salvo el final.

    """
    idx = df.index.astype(int)
    min_year, max_year = idx.min(), idx.max()

    # 1) solo los años dentro del rango
    in_range = sorted({yr for yr in years if min_year <= yr <= max_year})

    # 2) quedarnos solo con los que estén *strictly* entre min y max
    mid_years = [yr for yr in in_range if min_year < yr < (max_year-2)]

    # 3) reconstruir lista con min + medios + max
    return [min_year] + mid_years + [max_year]


def get_df(
    sql: str,
    conn_str: str,
    *,
    index_col: str | None = "año",
    rename: dict[str, str] | None = None,
    scale: dict[str, float] | None = None,
    compute_sum: dict[str, list[str]] | None = None,
    pivot: dict | None = None,
    sort_index: bool = True,
) -> pd.DataFrame:
    """Execute a SQL query and return a cleaned ``DataFrame``.

    Parameters
    ----------
    sql : str
        SQL query to run against the SQLite database.
    conn_str : str
        Path to the SQLite database file.
    index_col : str, optional
        Column to use as index. If ``None`` the index is left untouched.
    rename : dict[str, str], optional
        Mapping of columns to rename ``{old: new}``.
    scale : dict[str, float], optional
        Multiplicative factors for columns ``{col: factor}``.
    compute_sum : dict[str, list[str]], optional
        New columns defined as the sum of other columns.
    pivot : dict, optional
        Parameters for ``DataFrame.pivot_table`` such as ``index``, ``columns``,
        ``values``, ``aggfunc`` and ``fill_value``.
    sort_index : bool, optional
        Whether to sort the resulting ``DataFrame`` by the index column.

    Returns
    -------
    pd.DataFrame
        The processed DataFrame.
    """

    with sqlite3.connect(conn_str) as conn:
        df = pd.read_sql(sql, conn)

    if pivot:
        df = df.pivot_table(
            index=pivot.get("index"),
            columns=pivot.get("columns"),
            values=pivot.get("values"),
            aggfunc=pivot.get("aggfunc", "sum"),
            fill_value=pivot.get("fill_value", 0),
        )

    if rename:
        df = df.rename(columns=rename)

    if index_col and index_col in df.columns:
        df = df.set_index(index_col)
        if sort_index:
            df = df.sort_index()

    if scale:
        for col, factor in scale.items():
            if col in df.columns:
                df[col] = df[col] * factor

    if compute_sum:
        for new_col, cols in compute_sum.items():
            missing = [c for c in cols if c not in df.columns]
            if not missing:
                df[new_col] = df[cols].sum(axis=1)

    return df


def set_style() -> None:
    """
    Configura el estilo global de Matplotlib:
    - theme: 'seaborn-v0_8-whitegrid'
    - font_family: 'serif'
    - font_size: 12
    - dpi: 150
    """
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({
    'font.family':  'serif',
    'font.size':    12,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'grid.linestyle': '--',
    'lines.linewidth': 2,
    'figure.dpi':   150,
    'savefig.bbox': 'tight',
    })
def init_base_plot(
    df,
    series: list[tuple[str,str]],
    colors: dict[str,str],
    title: str, 
    xlabel: str,
    ylabel: str,
    figsize: tuple[int,int]=(13,8),
    legend_loc: str="upper left",
    legend_ncol: int=3,
    legend_fontsize: int=13.2,
    source_text: str="Fuente: Elaboración propia con datos de UDAPE",
    notas: str | None = None 
):
    """
    Inicializa fig y ax con:
     - series: lista de tuplas (columna, etiqueta)
     - colors: dict columna→color
     - titulación de ejes y leyenda
     - pie de fuente
    """
    fig, ax = plt.subplots(figsize=figsize)
    for col, label in series:
        ax.plot(df.index, df[col], label=label, color=colors[col])

    ax.set_title(title, fontweight='bold', color='red', fontsize=17)
    ax.set_xlabel(xlabel, color='green',fontsize=17)
    ax.set_ylabel(ylabel, color='blue', fontsize=17)
    ax.set_xticks(df.index[::max(1, len(df)//31)])
    ax.tick_params(axis='x', rotation=45)
    ax.legend(loc=legend_loc, ncol=legend_ncol, fontsize=legend_fontsize)

    fig.text(
        0.07, 0.005,
        source_text,
        ha="left", va="bottom",
        fontsize=12, color="black",
        transform=fig.transFigure
    )
    if notas:
    # calculamos una “altura” relativa al tamaño de la fuente de la nota
        line_height = 0.018          # ≈ 2 % de la altura de la figura
        nota_y = 0.005 - line_height # coloca la nota justo debajo de la fuente

        fig.text(
            0.07, nota_y,
            notas,
            ha="left", va="bottom",
            fontsize=11.5, color="black",
            transform=fig.transFigure,
        )
    plt.tight_layout()
    return fig, ax
def plot_stacked_bar(
    data: pd.DataFrame,
    series: List[Tuple[str, str]], 
    title: str,
    ylabel: str = "Participación (%)",
    xlabel: str = "Año",
    figsize: tuple = (14, 7),
    legend_ncol: int = 6,
    xtick_step: int = 2,
    width: float = 0.8
):
    """
    Gráfico de barras apiladas (100 %) con etiquetas personalizadas.

    Parámetros
    ----------
    data : DataFrame
        Indexado por año. Debe contener todas las columnas listadas en `series`.
    series : list[tuple[str, str]]
        Tuplas (nombre_columna, etiqueta_legible) que definen:
        - orden de las capas.
        - texto de la leyenda.
    title, ylabel, xlabel, figsize, legend_ncol, xtick_step, width : ver antes.

    Devuelve
    --------
    fig, ax : objetos matplotlib.
    """
    # 1) Reordenamos y renombramos las columnas según `series`
    cols, labels = zip(*series)                    # desempaca listas
    df = data.loc[:, cols].copy()                  # respeta el orden
    df.columns = labels                            # sustituye por etiquetas legibles

    # 2) Graficamos
    fig, ax = plt.subplots(figsize=figsize)
    df.plot(kind="bar", stacked=True, ax=ax, width=width)

    # 3) Decoración
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title, fontweight="bold", pad=20, color="red", fontsize=17)

    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        ncol=legend_ncol,
        fontsize=10,
        frameon=False
    )
    fig.subplots_adjust(bottom=0.25, right=0.72)

    positions = np.arange(len(df.index))
    ax.set_xticks(positions[::xtick_step])
    ax.set_xticklabels(df.index[::xtick_step], rotation=45)

    plt.tight_layout()
    return fig, ax



def add_hitos_barras(
    ax: plt.Axes,
    index: Sequence[int],
    hitos_v: Dict[int, str],
    hitos_offset: Dict[int, Tuple[float, float]],
    hitos_text_x: Dict[int, float] = {},
    *,
    bar_width: float = 0.8,
    fallback_offset: Tuple[float, float] = (0.0, 0.82),
    line_kwargs: Optional[Dict] = None,
    text_kwargs: Optional[Dict] = None
):
    """
    Dibuja verticales y etiquetas de hitos sobre un gráfico de barras.

    Parameters
    ----------
    ax : plt.Axes
    index : Sequence[int]
        La secuencia de años (p.ej. df.index).
    hitos_v : dict[int, str]
        { año: etiqueta }.
    hitos_offset : dict[int, (dx, dy)]
        { año: (offset_x, offset_y_factor) }.
    hitos_text_x : dict[int, float]
        { año: offset_x_text } para ajustar la posición del texto.
    bar_width : float
        Ancho de barra (para centrar las líneas).
    annotate_labels : tuple[str]
        Qué etiquetas mostrar.
    fallback_offset : (dx, dy)
        Offset por defecto si un año no está en hitos_offset.
    line_kwargs : dict
        Parámetros para `ax.axvline`.
    text_kwargs : dict
        Parámetros para `ax.text`.
    """
    # defaults
    lk = {'color':'black','linewidth':2.5,'linestyle':'-','zorder':10}
    if line_kwargs:
        lk.update(line_kwargs)

    tk = {
        'fontsize':12, 'color':'black',
        'ha':'center','va':'bottom',
        'rotation':0, 'zorder':6,
        'bbox':{'facecolor':'white','alpha':0.85,'edgecolor':'none'}
    }
    if text_kwargs:
        tk.update(text_kwargs)

    # iterate over your hitos
    for yr, lbl in hitos_v.items():
        if yr not in index:
            continue

        # unpack offsets (dx in data‐coords, dy as fraction of y_max)
        dx, dy = hitos_offset.get(yr, fallback_offset)

        # compute the x position: bar index + half‐width + dx
        pos = list(index).index(yr)
        x = pos + bar_width/2 + dx

        # vertical line
        ax.axvline(x=x,**lk)

        y_max = ax.get_ylim()[1]
        dx_text = hitos_text_x.get(yr, 0)
        ax.text(
            x+dx_text,
            y_max * dy,
            lbl,
            transform=ax.transData,
            **tk
        )


# guarda esto en, por ejemplo, graficos_utils.py
def add_hitos(
    ax,
    index,
    hitos_v: dict[int, str],
    hitos_offset: dict[int, float],
    *,
    annotate_labels: tuple[str, ...] = ('Crisis',),
    fallback_offset: float = 0.82,
    line_kwargs: dict = None,
    text_kwargs: dict = None
):
    """
    Dibuja líneas verticales en los años de `hitos_v` sobre el Axes `ax`.
    Solo anota con texto los hitos cuyo label esté en `annotate_labels`.

    Parámetros
    ----------
    ax : matplotlib.axes.Axes
    index : Sequence[int]
        Índice de años disponibles (p. ej. df.index).
    hitos_v : dict[int, str]
        { año: etiqueta } para la línea vertical.
    hitos_offset : dict[int, float]
        { año: factor } para ubicar el texto en y (multiplica y_max).
    annotate_labels : tupla de str, opcional
        Etiquetas que se dibujarán como texto (por defecto ('Crisis',)).
    fallback_offset : float, opcional
        Offset por defecto si falta en `hitos_offset`.
    line_kwargs : dict, opcional
        kwargs para ax.axvline (color, ls, lw, zorder).
    text_kwargs : dict, opcional
        kwargs para ax.text (rotation, ha, va, fontsize, color, bbox, zorder).
    """
    default_lk = {
        'color':'gray',
        'linestyle':'--',
        'linewidth':1.1,
        'zorder':5
    }
    # valores por defecto
    if line_kwargs:
        default_lk.update(line_kwargs)
    line_kwargs = default_lk
    if text_kwargs is None:
        text_kwargs = {
            'rotation': 90, 'ha':'right', 'va':'top',
            'fontsize':14, 'color':'#1f77b4',
            'bbox':{'facecolor':'#f0f0f0','alpha':0.85,'edgecolor':'none'},
            'zorder':6
        }

    for yr, lbl in hitos_v.items():
        if yr in index:
            ax.axvline(x=yr, **line_kwargs)
            y_max = ax.get_ylim()[1]
            offset = hitos_offset.get(yr, fallback_offset)
            if lbl in annotate_labels:
                ax.text(yr, y_max * offset, lbl, **text_kwargs)

# TASA DE CRECIMIENTO PARA UN SOLO COMPONENTE
# graficos_utils.py  (versión con periodos = (vi, vf) )

def add_period_growth_annotations_multi(
    ax,
    df: pd.DataFrame,
    periodos: list[tuple[int, int]],
    cols: list[str],
    period_offsets: dict[str, tuple[float, float]],
    colors: dict[str, str],
    abbr_map: dict[str, str],
    *,
    fmt: str = "{vi}→{vf}: {tasa}%",
    header_kwargs: dict | None = None,
    text_kwargs: dict | None = None,
    line_spacing_ratio: float = 0.03
):
    """
    Parameters
    ----------
    ax : matplotlib.axes.Axes
    df : pd.DataFrame
    periodos : list of (vi, vf)
    cols : list of column names
    period_offsets : dict["vi-vf" -> (x_rel, y_frac)]
        Define para cada periodo la posición del cuadro de tasas:
        x_rel: año (float) donde centrar el bloque;
        y_frac: fracción de y_max para la coordenada vertical.
    colors : dict[col -> color]
    abbr_map : dict[col -> abbr]
    … (otros parámetros iguales que antes)
    """
    abbr_map     = abbr_map or {}
    header_kwargs = header_kwargs or {
        'ha':'left','va':'top',
        'fontsize':11.5,'fontweight':'bold',
        'color':'black','zorder':7
    }
    text_kwargs   = text_kwargs   or {
        'ha':'left','va':'top',
        'fontsize':14,'zorder':7
    }

    y_max        = ax.get_ylim()[1]
    line_spacing = y_max * line_spacing_ratio

    for vi, vf in periodos:
        key = f"{vi}-{vf}"
        if key not in period_offsets:
            continue
        x_rel, y_frac = period_offsets[key]
        x0 = x_rel
        y0 = y_max * y_frac

        # 1) Header
        ax.text(x0, y0, f"{vi}→{vf}", **header_kwargs)

        # 2) Bloque de tasas (una línea por componente)
        for i, col in enumerate(cols):
            v_ini = df.loc[vi, col]
            v_fin = df.loc[vf, col]
            umbral = 1e-2   # por ejemplo, 0.01
            if abs(v_ini) < umbral or abs(v_fin) < umbral:
                continue
            if pd.isna(v_ini) or pd.isna(v_fin) or v_ini == 0 or v_fin == 0:
                continue        # salta esta columna si falta dato útil
            tasa = round((df.loc[vf, col] / df.loc[vi, col] - 1) * 100)
            y = y0 - (i + 1) * line_spacing

            kw = text_kwargs.copy()
            kw['color'] = colors.get(col, kw.get('color'))
            abbr = abbr_map.get(col, col)

            ax.text(
                x0,
                y,
                fr"$r_{{{abbr}}}$: {tasa:.0f}%",
                **kw
            )



def add_cycle_means_multi(
    ax,
    cycle_stats: dict[str, dict[str, float]],
    text_offsets: dict[str, tuple[float, float]],
    abbr_map: dict[str, str],
    colors: dict[str, str],
    line_spacing: float,
    *,
    header_kwargs: dict | None = None,
    text_kwargs: dict | None = None,
    value_fmt: str = "{:,.0f}",
):
    """
    Anota en `ax` las medias por ciclo para múltiples componentes.

    Parámetros
    ----------
    ax : matplotlib.axes.Axes
    cycle_stats : dict[str, dict[str, float]]
        { nombre_ciclo: { componente: media } }
    text_offsets : dict[str, (x, y)]
        Coordenadas (data) donde colocar cada bloque de texto por ciclo.
    abbr_map : dict[str, str]
        { componente: abreviatura_para_subíndice }
    colors : dict[str, str]
        { componente: color_del_texto }
    line_spacing : float
        Desplazamiento vertical entre líneas sucesivas (en unidades de datos).
    header_kwargs : dict, opcional
        kwargs para el texto del título de cada ciclo.
    text_kwargs : dict, opcional
        kwargs base para el texto de cada media (el color se actualiza por componente).
    value_fmt : str, opcional
        Formato para representar el valor numérico
        (default = "{:,.0f}"  →  sin decimales; usa p. ej. "{:,.2f}" para 2 decimales).
    """
    # valores por defecto
    header_kwargs = header_kwargs or {
        'ha': 'left', 'va': 'top',
        'fontsize': 11.5, 'fontweight': 'bold',
        'color': 'red', 'zorder': 7
    }
    text_kwargs = text_kwargs or {
        'ha': 'left', 'va': 'top',
        'fontsize': 14, 'zorder': 7
    }
    for ciclo, stats in cycle_stats.items():
        if ciclo not in text_offsets:
            continue
        y_max = ax.get_ylim()[1]
        x0, y0 = text_offsets[ciclo]
        # 1) Título del ciclo
        ax.text(x0, y_max*y0, ciclo, **header_kwargs)
        # 2) Una línea por cada componente
        for i, comp in enumerate(stats):
            raw_val = stats[comp]
            val = value_fmt.format(raw_val)
            y = y_max*y0 - (i + 1) * line_spacing
            params = text_kwargs.copy()
            params['color'] = colors.get(comp, params.get('color'))
            abbr = abbr_map.get(comp, comp)
            ax.text(
                x0,
                y,
                fr"$\bar{{x}}_{{{abbr}}}$: {val}",
                **params
            )



# guarda esto en graficos_utils.py ────────────────────────────────────────────
def add_year_value_annotations(
    ax,
    df,
    years: list[int],
    columnas: list[str],
    annotation_offsets: dict[str, dict[int, tuple[float, float]]],
    colors: dict[str, str],
    *,
    value_fmt: str = "{:,.0f}",
    arrow_lw: float = 1.1,
    text_kwargs: dict | None = None,
    arrowprops_extra: dict | None = None,
):
    """
    Anota los valores de cada sector en los años especificados.

    Parámetros
    ----------
    ax : matplotlib.axes.Axes
        El eje donde se añaden las anotaciones.
    df : pandas.DataFrame
        Índice de años, columnas = columnas (columna interna de cada tupla).
    years : list[int]
        Años que se desean anotar.
    columnas: list[str],
        Lista (en el mismo orden que se ploteó) con nombre de columna.
    annotation_offsets : dict[str, dict[int, (dx, dy)]]
        Offsets de texto personalizados: {col: {año: (dx, dy)}}.
    colors : dict[str, str]
        {col: color_hex} para cada sector.
    value_fmt : str, opcional
        Formato del texto numérico.
    arrow_lw : float, opcional
        Grosor de la línea flecha.
    text_kwargs : dict, opcional
        kwargs adicionales para `ax.annotate` (fontsize, ha, etc.).
    arrowprops_extra : dict, opcional
        Opciones adicionales para arrowprops que se combinan con arrow_lw.

    Ejemplo de uso
    --------------
    from graficos_utils import add_year_value_annotations
    add_year_value_annotations(ax, df, anot_years, columnas,
                               annotation_offsets, custom_colors)
    """

    # defaults
    if text_kwargs is None:
        text_kwargs = {'ha': 'center', 'va': 'center', 'fontsize': 14}
    if arrowprops_extra is None:
        arrowprops_extra = {}

    # arrow base dict
    def arrowprops(color):
        base = dict(arrowstyle='-', color=color, lw=arrow_lw)
        base.update(arrowprops_extra)
        return base

    for yr in years:
        if yr not in df.index:
            continue

        # Ordenar valores de menor a mayor para colocar flechas "escalonadas"
        vals = [(df.loc[yr, col], col) for col in columnas]
        vals.sort(key=lambda t: t[0])
        for y, col in vals:
            offsets_for_col = annotation_offsets.get(col)
            if not offsets_for_col or yr not in offsets_for_col:
                continue
            dx, dy = offsets_for_col[yr]
            ax.annotate(
                value_fmt.format(y),
                xy=(yr, y),
                xytext=(yr + dx, y + dy),
                arrowprops=arrowprops(colors[col]),
                color=colors[col],
                **text_kwargs
            )

def add_participation_cycle_boxes(
    ax,
    df: pd.DataFrame,
    periods: list[tuple[int, int]],
    components: list[str],
    total_col: str,
    offsets: dict[str, tuple[float, float]],
    abbr_map: dict[str, str] | None = None,
    colors: dict[str, str] | None = None,
    *,
    header_kwargs: dict | None = None,
    text_kwargs: dict | None = None,
    line_spacing: float = 0.03,
):
    """
    Dibuja por cada ciclo un recuadro con la participación media (%) de cada componente.

    Parámetros
    ----------
    ax : matplotlib.axes.Axes
        El eje sobre el que se tracen los textos.
    df : pandas.DataFrame
        DataFrame con índice de años y columnas para cada componente y la columna total.
    periods : list of (vi, vf)
        Lista de tuplas (vi, vf) que definen los periodos para cada ciclo.
    components : list[str]
        Lista de nombres de columna que corresponden a los componentes cuyos porcentajes se calcularán.
    total_col : str
        Nombre de la columna en `df` que contiene el total sobre el que calcular el porcentaje.
    offsets : dict[str, tuple[float, float]]
        Posición en el gráfico para cada recuadro:
        { nombre_ciclo: (x_rel, y_frac) }, donde
        x_rel es el año en coordenadas de datos
        y_frac es la fracción de la altura del eje (0–1).
    abbr_map : dict[str, str], opcional
        Mapa de cada columna a su abreviatura para subíndices en el texto;
        si es None, usa el nombre de columna tal cual.
    colors : dict[str, str], opcional
        Color de texto para cada componente;
        si es None, toma el color de la primera línea trazada en el eje.
    header_kwargs : dict, opcional
        kwargs para `ax.text` del encabezado (nombre de ciclo).
    text_kwargs : dict, opcional
        kwargs para `ax.text` de los porcentajes de cada componente.
    line_spacing : float, opcional
        Espacio vertical entre líneas de texto, en unidades de datos.

    Comportamiento
    -------------
    1. Para cada (ciclo, slice) en `periods`:
       a. Extrae `df_period = df.loc[slice, components + [total_col]]` y descarta filas incompletas.
       b. Calcula `pct = (df_period[components] / df_period[total_col]) * 100` año a año.
       c. Media de esos porcentajes: `medias_pct = pct.mean()`.
    2. Ubica el recuadro en `(x0, y0)` calculado con `offsets[ciclo]` y `y_max`.
    3. Dibuja el nombre del ciclo y, fila a fila, el texto `"%_{abbr}: value%"` con color.
    """
    abbr_map     = abbr_map or {c: c for c in components}
    colors       = colors   or {c: ax.get_lines()[0].get_color() for c in components}
    header_kwargs= header_kwargs or {
        'ha':'left','va':'top','fontsize':11.5,'fontweight':'bold','color':'black','zorder':7
    }
    text_kwargs  = text_kwargs   or {
        'ha':'left','va':'top','fontsize':15,'zorder':7
    }

    y_max        = ax.get_ylim()[1]
    line_spacing = y_max * line_spacing

    for vi, vf in periods:
        # crea el slice de años y la clave para offsets
        period_slice = slice(vi, vf)
        key = f"{vi}-{vf}"
        # validar existencia de offset
        if key not in offsets:
            continue
        # recorta datos y calcula %
        df_period = df.loc[period_slice, components + [total_col]].dropna()
        pct = df_period[components].div(df_period[total_col], axis=0) * 100
        medias_pct = pct.mean()

        # offset
        x0, y_frac = offsets[key]
        y0 = y_max * y_frac
        short_vi = str(vi)[2:]
        short_vf = str(vf)[2:]
        # encabezado compacto en modo LaTeX
        header = rf"$\bar{{p}} $ {short_vi}–{short_vf}"
        ax.text(x0, y0, header, **header_kwargs)
        for i, comp in enumerate(components):
            pct_med = medias_pct[comp]
            y = y0 - (i+1)*line_spacing
            txt = fr"$\bar{{x}}_{{{abbr_map.get(comp,comp)}}}$: {pct_med:.0f}%"
            kw = text_kwargs.copy()
            kw['color'] = colors.get(comp, kw.get('color'))
            ax.text(x0, y, txt, **kw)