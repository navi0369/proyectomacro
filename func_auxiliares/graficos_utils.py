import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.axes import Axes
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


def add_period_backgrounds(
    ax: Axes,
    periods: Sequence[Tuple[int, int]] | Sequence[slice]=["Cyan","Magenta","green","Black"],
    colors: Mapping[Tuple[int, int] | str, str] | Sequence[str]=["Cyan","Magenta","green","Black"],
    *,
    index: Sequence[int] | None = None,
    alpha: float = 0.064,
    zorder: int = 0,
    edgecolor: str | None = None,
    linewidth: float = 0.0,
    label_fmt: str | None = None,
) -> None:
    """
    Dibuja fondos de color por periodo sobre el eje.

    Parameters
    ----------
    ax : plt.Axes
        Eje donde se pintan los fondos.
    periods : Sequence[(ini, fin)] | Sequence[slice]
        Periodos en años. Si se pasan slices, se usan start/stop.
    colors : Mapping | Sequence
        - Si es Mapping: puede usar claves (ini, fin) o "ini-fin".
        - Si es Sequence: se asigna por orden a `periods`.
    index : Sequence[int], opcional
        Años disponibles para recortar los periodos al rango real.
    alpha : float
        Transparencia del fondo.
    zorder : int
        Orden de pintado (menor = más al fondo).
    edgecolor : str | None
        Color de borde del rectángulo (si None, sin borde).
    linewidth : float
        Grosor del borde.
    label_fmt : str | None
        Si se pasa, agrega label en leyenda usando el formato
        (ej. "{start}-{end}").
    """
    if not periods:
        return

    if isinstance(periods, Mapping):
        period_items = list(periods.items())
    else:
        period_items = [(None, p) for p in periods]

    use_map = isinstance(colors, Mapping)
    if not use_map and len(colors) < len(period_items):
        raise ValueError("colors debe tener al menos un color por periodo")

    idx_min, idx_max = ax.get_xlim()
    if index is not None:
        idx_vals = list(map(int, index))
        if idx_vals:
            idx_min, idx_max = min(idx_vals), max(idx_vals)

    def _normalize_period(p: Tuple[int, int] | slice) -> Tuple[int, int]:
        if isinstance(p, slice):
            start, end = int(p.start), int(p.stop)
        else:
            start, end = map(int, p)
        if idx_min is not None and idx_max is not None:
            start = max(start, int(idx_min))
            end = min(end, int(idx_max))
        return start, end

    for i, (name, p) in enumerate(period_items):
        start, end = _normalize_period(p)
        if start >= end:
            continue

        if use_map:
            color = colors.get(name)
            if color is None:
                color = colors.get((start, end))
            if color is None:
                color = colors.get(f"{start}-{end}")
        else:
            color = colors[i]

        if color is None:
            continue

        label = label_fmt.format(start=start, end=end) if label_fmt else None
        ax.axvspan(
            start,
            end,
            facecolor=color,
            alpha=alpha,
            zorder=zorder,
            edgecolor=edgecolor,
            linewidth=linewidth,
            label=label,
        )



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
        cum_pos = 0.0                               # acumulado para positivos
        cum_neg = 0.0                               # acumulado para negativos
        for col in cols:
            if skip and col in skip.get(name, set()):
                val = stats[col]
                if val >= 0:
                    cum_pos += val
                else:
                    cum_neg += val
                continue

            val = stats[col]
            dx, dy = (0.0, 0.0)
            if offsets:
                off_val = offsets.get(name, {}).get(col, (0.0, 0.0))
                if isinstance(off_val, tuple) and len(off_val) == 2:
                    dx, dy = off_val

            if val >= 0:
                y_pos = cum_pos + val / 2
                cum_pos += val
            else:
                y_pos = cum_neg + val / 2
                cum_neg += val

            ax.text(
                x_mid + dx,
                y_pos + dy,
                fmt.format(val=val),
                transform=ax.transData,
                **text_kwargs
            )
def adjust_cycles(df: pd.DataFrame,
 cycles: dict[str, slice]) -> dict[str, slice]:
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
            cycles_adj[name] = slice(start, stop_incl)
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
    color: str = "red",
    fontsize: int = 17,
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

    ax.set_title(title, fontweight='bold', color=color,pad=20, fontsize=fontsize)
    ax.set_xlabel(xlabel, color='green',fontsize=17)
    ax.set_ylabel(ylabel, color='blue', fontsize=17)
    
    # Paso dinámico según longitud de la serie
    n = len(df)
    if n <= 36:
        step = 1
    elif n <= 77:
        step = 2
    else:
        step = 3
    years = df.index.tolist()
    last_year = years[-1]
    first_year = years[0]
    # Genera ticks regulares desde el primer año con el paso elegido
    tick_years = list(range(first_year, last_year, step))
    tick_positions = [float(y) for y in tick_years]
    tick_labels = [str(y) for y in tick_years]
    
    # Garantiza que el último año esté siempre presente (sin duplicar)
    if last_year not in tick_years:
        if tick_years and (last_year - tick_years[-1] == 1) and step > 1:
            # Desplaza un poco a la derecha para que no se solape con el año anterior
            tick_positions.append(last_year + 0.35)
        else:
            tick_positions.append(float(last_year))
        tick_labels.append(str(last_year))
        
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)

    ax.tick_params(axis='x', rotation=45)
    
    if len(series) > 1:
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
    fig.subplots_adjust(bottom=0.25)

    positions = np.arange(len(df.index))
    ax.set_xticks(positions[::xtick_step])
    ax.set_xticklabels(df.index[::xtick_step], rotation=45)

    plt.tight_layout()
    return fig, ax

def init_dual_axis_plot(
    df: pd.DataFrame,
    left_series: list[tuple[str, str]],
    right_series: list[tuple[str, str]],
    colors: dict[str, str],
    title: str,
    xlabel: str,
    left_ylabel: str,
    right_ylabel: str,
    figsize: tuple[int, int] = (13, 8),
    legend_loc: str = "upper left",
    legend_ncol: int = 2,
    legend_fontsize: int = 12,
    source_text: str = "Fuente: Elaboración propia",
    notas: str | None = None
):
    """
    Gráfica “dual axis” (dos ejes Y) reutilizando el mismo estilo
    que `init_base_plot`.

    Parámetros
    ----------
    df : DataFrame
        Con índice en años y columnas suficientes para ambas listas.
    left_series : list[(col, label)]
        Series que se pintan en el eje Y izquierdo.
    right_series : list[(col, label)]
        Series que se pintan en el eje Y derecho.
    colors : dict[col -> color]
        Paleta para todas las series (tanto izquierda como derecha).
    title, xlabel, left_ylabel, right_ylabel : str
        Textos de títulos y ejes.
    figsize, legend_loc, legend_ncol, legend_fontsize : estilos varios.
    source_text : str
        Pie de fuente.
    notas : str | None
        Texto opcional que aparece debajo de la fuente.

    Devuelve
    --------
    fig, ax_left, ax_right
    """

    # 1) Figura y ejes (ax_left + ax_right)
    fig, ax_left = plt.subplots(figsize=figsize)
    ax_right = ax_left.twinx()

    # 2) Traza series del eje izquierdo
    for col, label in left_series:
        ax_left.plot(df.index, df[col], label=label, color=colors[col])

    # 3) Traza series del eje derecho
    for col, label in right_series:
        ax_right.plot(df.index, df[col], label=label, color=colors[col])

    # 4) Títulos y ejes
    ax_left.set_title(title, fontweight="bold", fontsize=17,pad=20, color="red")
    ax_left.set_xlabel(xlabel, fontsize=15)
    ax_left.set_ylabel(left_ylabel, color="tab:blue", fontsize=14)
    ax_right.set_ylabel(right_ylabel, color="tab:red", fontsize=14)

    # 5) Estilo de ticks
    ax_left.tick_params(axis="y", labelcolor="tab:blue")
    ax_right.tick_params(axis="y", labelcolor="tab:red")
    
    # Paso dinámico según longitud de la serie
    n = len(df)
    if n <= 36:
        step = 1
    elif n <= 77:
        step = 2
    else:
        step = 3
    years = df.index.tolist()
    last_year = years[-1]
    first_year = years[0]
    # Genera ticks regulares desde el primer año con el paso elegido
    tick_years = list(range(first_year, last_year, step))
    tick_positions = [float(y) for y in tick_years]
    tick_labels = [str(y) for y in tick_years]
    
    # Garantiza que el último año esté siempre presente (sin duplicar)
    if last_year not in tick_years:
        if tick_years and (last_year - tick_years[-1] == 1) and step > 1:
            # Desplaza un poco a la derecha para que no se solape con el año anterior
            tick_positions.append(last_year + 0.35)
        else:
            tick_positions.append(float(last_year))
        tick_labels.append(str(last_year))
        
    ax_left.set_xticks(tick_positions)
    ax_left.set_xticklabels(tick_labels)
    ax_left.tick_params(axis="x", rotation=45)

    # 6) Leyenda combinada (sin duplicados)
    h_left, l_left = ax_left.get_legend_handles_labels()
    h_right, l_right = ax_right.get_legend_handles_labels()
    h_comb, l_comb = [], []
    for h, l in zip(h_left + h_right, l_left + l_right):
        if l not in l_comb:          # evita duplicados
            h_comb.append(h)
            l_comb.append(l)

    ax_left.legend(
        h_comb, l_comb,
        loc=legend_loc,
        ncol=legend_ncol,
        fontsize=legend_fontsize
    )

    # 7) Pie de fuente
    fig.text(
        0.07, 0.005, source_text,
        ha="left", va="bottom",
        fontsize=11, transform=fig.transFigure
    )

    # 8) Nota opcional
    if notas:
        fig.text(
            0.07, -0.02, notas,
            ha="left", va="bottom",
            fontsize=10.5, transform=fig.transFigure
        )

    plt.tight_layout()
    return fig, ax_left, ax_right



def add_hitos_barras(
    ax: plt.Axes,
    index: Sequence[int],
    hitos_v: Dict[int, str],
    hitos_offset: Dict[int, Tuple[float, float]] = None,
    hitos_text_x: Dict[int, float] = None,
    *,
    annotate_labels: tuple[str, ...] = ('INTERVENSIONISMO ESTATAL', 'NEOLIBERALISMO', 'E.S.C.P (I)', 'E.S.C.P (II)'),
    bar_width: float = 0.8,
    fallback_offset: Tuple[float, float] = (0.0, 0.82),
    line_kwargs: Optional[Dict] = None,
    text_kwargs: Optional[Dict] = None
):
    """
    Dibuja verticales y etiquetas de hitos sobre un gráfico de barras.
    Alinea el texto en el centro del período (como add_hitos).
    """
    if hitos_offset is None:
        hitos_offset = {}
    if hitos_text_x is None:
        hitos_text_x = {}

    lk = {'color':'black','linewidth':2.5,'linestyle':'-','zorder':10}
    if line_kwargs:
        lk.update(line_kwargs)

    tk = {
        'fontsize':12, 'color':'black',
        'ha':'center','va':'bottom',
        'rotation':0, 'zorder':6,
    }
    if text_kwargs:
        tk.update(text_kwargs)

    index_list = sorted(list(index))
    index_set  = set(index_list)
    last_year  = index_list[-1] if index_list else None

    # Derivar los rangos de periodo
    hito_years = sorted(hitos_v.keys())
    periodos: dict[int, tuple[int, int]] = {}
    for i, yr in enumerate(hito_years):
        fin = (hito_years[i + 1] - 1) if i + 1 < len(hito_years) else last_year
        periodos[yr] = (yr, fin)

    for yr, lbl in hitos_v.items():
        yr_in_data = yr in index_set
        inicio, fin = periodos.get(yr, (yr, yr))
        available = [y for y in index_list if inicio <= y <= fin]

        if not yr_in_data and not available:
            continue

        y_max = ax.get_ylim()[1]

        # 1. Línea vertical
        if yr_in_data:
            dx, dy = hitos_offset.get(yr, fallback_offset)
            pos = list(index).index(yr)
            x_line = pos + bar_width/2 + dx
            ax.axvline(x=x_line, **lk)

        # 2. Posición X del texto
        if available:
            pos_first = list(index).index(available[0])
            pos_last = list(index).index(available[-1])
            x_texto = (pos_first + pos_last) / 2
        elif yr_in_data:
            pos = list(index).index(yr)
            x_texto = pos + hitos_text_x.get(yr, 0)
        else:
            continue

        # 3. Texto
        if lbl in annotate_labels:
            ax.text(x_texto, y_max * 1.01, lbl, transform=ax.transData, **tk)


def add_hitos(
    ax,
    index,
    hitos_v: dict[int, str],
    hitos_offset: dict[int, float] = None,
    hitos_text_x: dict[int, float] = None,
    *,
    annotate_labels: tuple[str, ...] = ('INTERVENSIONISMO ESTATAL', 'NEOLIBERALISMO', 'E.S.C.P (I)', 'E.S.C.P (II)'),
    fallback_offset: float = 1.02,
    line_kwargs: dict = None,
    text_kwargs: dict = None
):
    """
    Dibuja líneas verticales en los años de ``hitos_v`` sobre el Axes ``ax``.
    Solo anota con texto los hitos cuyo label esté en ``annotate_labels``.

    Los periodos sobre los que se promedia la posición X del texto se derivan
    **automáticamente** de ``hitos_v``:

    * El periodo de cada hito comienza en su propio año de inicio y termina
      un año antes del siguiente hito (o en el último año disponible en
      ``index`` para el hito final).
    * Si el periodo está incompleto (el año de inicio no aparece en los datos
      pero sí hay datos dentro del rango), el texto se coloca en el punto
      medio entre el primer año disponible y el fin del periodo.

    Parámetros
    ----------
    ax : matplotlib.axes.Axes
    index : sequence of int
        Años presentes en el DataFrame (p.ej. ``df.index``).
    hitos_v : dict[int, str]
        ``{ año_inicio: etiqueta }`` — **debe estar ordenado** (Python 3.7+).
    hitos_offset : dict[int, float]
        ``{ año: fracción_y }`` — multiplicador de ``y_max`` para la altura
        del texto. Se usa el ``fallback_offset`` si el año no está.
    hitos_text_x : dict[int, float], opcional
        Desplazamiento manual en X para casos sin datos en el rango.
        Solo se aplica como último recurso.
    annotate_labels : tuple[str]
        Solo se agrega texto para los hitos cuyo label esté en esta tupla.
    fallback_offset : float
        Fracción de ``y_max`` por defecto cuando el año no está en
        ``hitos_offset``.
    line_kwargs, text_kwargs : dict, opcional
        Kwargs extra para ``axvline`` y ``ax.text`` respectivamente.
    """
    if hitos_text_x is None:
        hitos_text_x = {}

    default_lk = {
        'color': 'gray',
        'linestyle': '--',
        'linewidth': 1.1,
        'zorder': 5
    }
    if line_kwargs:
        default_lk.update(line_kwargs)
    line_kwargs = default_lk

    if text_kwargs is None:
        text_kwargs = {
            'rotation': 0,
            'ha': 'center',
            'va': 'bottom',
            'fontsize': 12,
            'color': 'black',
            'bbox': {'facecolor': 'white', 'alpha': 0.85, 'edgecolor': 'none'},
            'zorder': 6
        }

    index_list = sorted(index)          # lista ordenada de años disponibles
    index_set  = set(index_list)
    last_year  = index_list[-1] if index_list else None

    # ── Derivar los rangos de periodo desde hitos_v ──────────────────────────
    # hitos_v = { yr0: lbl0, yr1: lbl1, ... } ordenado por año
    hito_years = sorted(hitos_v.keys())
    periodos: dict[int, tuple[int, int]] = {}
    for i, yr in enumerate(hito_years):
        fin = (hito_years[i + 1] - 1) if i + 1 < len(hito_years) else last_year
        periodos[yr] = (yr, fin)

    # ── Dibujar cada hito ─────────────────────────────────────────────────────
    for yr, lbl in hitos_v.items():
        yr_in_data = yr in index_set

        inicio, fin = periodos.get(yr, (yr, yr))
        available   = [y for y in index_list if inicio <= y <= fin]

        # Si no hay el año de inicio NI datos dentro del rango, saltar
        if not yr_in_data and not available:
            continue

        y_max  = ax.get_ylim()[1]

        # 1. Línea vertical (solo si el año de inicio existe en los datos)
        if yr_in_data:
            ax.axvline(x=yr, **line_kwargs)

        # 2. Posición X del texto
        if available:
            # Punto medio entre el primer y último año disponible del periodo
            x_texto = (available[0] + available[-1]) / 2
        elif yr_in_data:
            x_texto = yr + hitos_text_x.get(yr, 0)
        else:
            continue

        # 3. Texto (solo para etiquetas configuradas)
        if lbl in annotate_labels:
            ax.text(x_texto, y_max * 1.01, lbl, **text_kwargs)

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
        'color':'green','zorder':7
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
        ax.text(x0, y0, f"TASA DE\nCRECIMIENTO", **header_kwargs)
        offset_header = 1
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
            y = y0 - (i + 1 + offset_header) * line_spacing

            kw = text_kwargs.copy()
            kw['color'] = colors.get(col, kw.get('color'))
            abbr = abbr_map.get(col, col)

            ax.text(
                x0,
                y,
                fr"{abbr}: {tasa:.0f}%",
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
    extra_line_space: int = 0,
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
    extra_line_space : int, opcional
        Extra line space between the means.
        (default = 0)
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
        ax.text(x0, y_max*y0, "MEDIAS", **header_kwargs)
        # 2) Una línea por cada componente
        for i, comp in enumerate(stats):
            raw_val = stats[comp]
            val = value_fmt.format(raw_val)
            y = y_max*y0 - (i + 1 + extra_line_space) * line_spacing
            params = text_kwargs.copy()
            params['color'] = colors.get(comp, params.get('color'))
            abbr = abbr_map.get(comp, comp)
            ax.text(
                x0,
                y,
                f"{abbr}: {val}",
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