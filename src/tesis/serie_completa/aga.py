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