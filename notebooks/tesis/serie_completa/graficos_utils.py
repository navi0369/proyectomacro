import pandas as pd
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import sqlite3
from pathlib import Path

# graficos_utils.py

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


def save_fig(
    fig: plt.Figure,
    fname: str,
    base_dir: str = "assets",
    fmt: str = "png",
    dpi: int = 300
) -> None:
    """
    Guarda una figura de Matplotlib en disco.

    Parámetros
    ----------
    fig : matplotlib.figure.Figure
        Figura a guardar.
    fname : str
        Ruta y nombre de archivo sin extensión (p.ej. 'tesis/grafico1').
    base_dir : str
        Directorio base donde guardar (crea subcarpetas si no existen).
    fmt : str
        Formato de archivo (p.ej. 'png', 'pdf').
    dpi : int
        Resolución de la imagen.
    """
    path = Path(base_dir) / f"{fname}.{fmt}"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi)
    plt.close(fig)


def cycle_stats(
    df: pd.DataFrame,
    periods: list[tuple[int, int]],
    cols: list[str],
    kind: str = "mean"
) -> dict[str, dict[str, float]]:
    """
    Calcula estadísticas por ciclo para columnas dadas.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame con índice de años.
    periods : list of (int, int)
        Lista de tuplas (inicio, fin) de periodos.
    cols : list[str]
        Columnas sobre las que calcular estadísticas.
    kind : str
        Tipo de estadística: 'mean', 'growth'.

    Devuelve
    --------
    dict[str, dict[str, float]]
        { 'vi-vf': {col: valor} } donde valor = media o tasa de crecimiento.
    """
    stats = {}
    for vi, vf in periods:
        key = f"{vi}-{vf}"
        sub = df.loc[vi:vf, cols]
        if kind == "mean":
            stats[key] = sub.mean().to_dict()
        elif kind == "growth":
            stats[key] = ((sub.loc[vf] / sub.loc[vi] - 1) * 100).to_dict()
    return stats


def plot_dual_axis(
    df: pd.DataFrame,
    y1: str,
    y2: str,
    *,
    title: str,
    colors: dict[str, str],
    periods: list[tuple[int, int]],
    hitos: dict[str, dict],
    out: str,
    base_dir: str = "assets"
) -> None:
    """
    Genera y guarda un gráfico con eje dual (y1 vs y2).

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame con índice de años y columnas y1, y2.
    y1 : str
        Nombre de la columna para el eje izquierdo.
    y2 : str
        Nombre de la columna para el eje derecho.
    title : str
        Título del gráfico.
    colors : dict[str, str]
        Colores para y1 y y2 {col: color_hex}.
    periods : list of (int, int)
        Periodos para anotaciones de ciclo.
    hitos : dict[str, dict]
        Diccionario con claves:
        - 'labels': {año: etiqueta}
        - 'offsets': {año: factor}
        - 'cycle_txt_off': {periodo: (x, y_frac)}
    out : str
        Ruta y nombre de archivo (sin extensión) para guardar.
    base_dir : str
        Directorio base donde escribir la imagen.
    """
    fig, ax1 = plt.subplots(figsize=(12, 7))
    ax2 = ax1.twinx()

    ax1.plot(df.index, df[y1], label=y1, color=colors[y1])
    ax2.plot(df.index, df[y2], label=y2, color=colors[y2])

    add_hitos(ax1, df.index, hitos['labels'], hitos['offsets'])

    stats = cycle_stats(df, periods, [y1, y2], kind="mean")
    add_cycle_means_multi(
        ax1,
        stats,
        hitos['cycle_txt_off'],
        {y1: 'Y1', y2: 'Y2'},
        colors,
        line_spacing=df[y1].max() * 0.03,
        value_fmt="{:.1f}"
    )

    ax1.set_title(title, fontweight="bold")
    ax1.set_xlabel("Año")
    ax1.set_ylabel(y1, color=colors[y1])
    ax2.set_ylabel(y2, color=colors[y2])
    ax1.tick_params(axis="x", rotation=45)

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, loc="upper left")

    fig.tight_layout()
    save_fig(fig, out, base_dir=base_dir)

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
            dx, dy = annotation_offsets.get(col, {}).get(yr, (0, 0))
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