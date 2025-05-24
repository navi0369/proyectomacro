import pandas as pd
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
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
    text_kwargs: dict | None = None
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
            val = int(round(stats[comp]))
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