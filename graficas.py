import matplotlib.pyplot as plt
import io
import base64

def create_line_plot(
    df,
    y_col,
    title,
    xlabel,
    ylabel,
    annotations=None,
    *,
    x_col=None,
    annotate_bottom_years=None,
    annotate_top_years=None,
    fill_ranges=None,
    figsize=(15, 7.5),
    line_options=None
):
    """
    Genera un gráfico de línea con anotaciones y áreas sombreadas.

    Parámetros:
    - df: DataFrame que contiene los datos.
    - y_col: Nombre de la columna para el eje Y.
    - title: Título del gráfico.
    - xlabel: Etiqueta del eje X.
    - ylabel: Etiqueta del eje Y.
    - x_col: Nombre de la columna para el eje X. Si es None, se usa df.index.
    - annotate_bottom_years: Lista de valores (años) para anotar con va='bottom'.
    - annotate_top_years: Lista de valores (años) para anotar con va='top'.
    - fill_ranges: Lista de diccionarios con los rangos a sombrear. Cada diccionario debe contener:
         'start': valor inicial,
         'end': valor final,
         'color': color del sombreado,
         'alpha': transparencia,
         'label': etiqueta (opcional).
    - figsize: Tamaño de la figura.
    - line_options: Diccionario con opciones para la línea (marker, color, linestyle, linewidth).

    Retorna:
    - fig, ax: La figura y el eje de matplotlib.
    """
    if x_col is None:
        x_vals = df.index
    else:
        x_vals = df[x_col]

    if line_options is None:
        line_options = {'marker': 'o', 'color': 'steelblue', 'linestyle': '-', 'linewidth': 2}

    fig, ax = plt.subplots(figsize=figsize)
    
    # Graficar la línea
    ax.plot(x_vals, df[y_col], label=ylabel, **line_options)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold', color=line_options.get('color', 'steelblue'))
    ax.grid(visible=True, linestyle='--', color='gray', alpha=0.3)
    ax.tick_params(axis='x', labelrotation=45)

    # Anotaciones con va='bottom'
    if annotate_bottom_years:
        for year in annotate_bottom_years:
            # Verificar si el año está presente
            if (x_col is None and year in df.index) or (x_col is not None and year in df[x_col].values):
                value = df.loc[df.index==year, y_col].values[0] if x_col is None else df.loc[df[x_col]==year, y_col].values[0]
                ax.text(year, value, f'{value}', ha='right', va='bottom' if value > 0 else 'top',
                        fontsize=11.8, color=line_options.get('color', 'steelblue'), fontweight='bold')
                
    # Anotaciones con va='top'
    if annotate_top_years:
        for year in annotate_top_years:
            if (x_col is None and year in df.index) or (x_col is not None and year in df[x_col].values):
                value = df.loc[df.index==year, y_col].values[0] if x_col is None else df.loc[df[x_col]==year, y_col].values[0]
                ax.text(year, value, f'{value}', ha='right', va='top',
                        fontsize=11.8, color=line_options.get('color', 'steelblue'), fontweight='bold')
                
    # Áreas sombreadas
    if fill_ranges:
        for fr in fill_ranges:
            start = fr.get('start')
            end = fr.get('end')
            color = fr.get('color', 'lightgray')
            alpha = fr.get('alpha', 0.5)
            label = fr.get('label', None)
            condition = (x_vals >= start) & (x_vals <= end)
            ax.fill_between(x_vals, df[y_col].min(), df[y_col].max(), where=condition,
                            color=color, alpha=alpha, label=label)
     # Agregar anotaciones si están definidas
    if annotations:
        for ann in annotations:
            # Si el usuario define x e y
            if 'x' in ann and 'y' in ann:
                x_val = ann['x']
                y_val = ann['y']
            
            # Sino, busca 'year' y extrae el valor de la serie en ese año
            elif 'year' in ann:
                year = ann['year']
                if x_col is not None and year in df[x_col].values:
                    x_val = year
                    y_val = df.loc[df[x_col] == year, y_col].values[0]
                elif x_col is None and year in df.index:
                    x_val = year
                    y_val = df.loc[year, y_col]
                else:
                    # Si no se cumple, no anotamos nada
                    continue
            else:
                # Si no hay ni 'x','y' ni 'year', no podemos anotar
                continue
            
            # Extraer el texto y otras propiedades
            text = ann.get('text', '')
            va = ann.get('va', 'top')
            ha = ann.get('ha', 'right')
            fontsize = ann.get('fontsize', 12)
            color = ann.get('color', 'black')
            
            # Crear la anotación
            ax.text(x_val, y_val, text, va=va, ha=ha, fontsize=fontsize, color=color, fontweight='bold')
    
    plt.tight_layout()
    return fig, ax

def fig_to_base64(fig):
    """Convierte una figura de Matplotlib en una imagen Base64 para mostrarla en Dash."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    encoded_string = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded_string}"