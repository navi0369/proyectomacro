# page_factory.py
from pathlib import Path
from typing import Dict, List

import dash
import dash_bootstrap_components as dbc
from dash import html, dash_table, get_asset_url
from extract_data import load_validated_tables, list_table_image_groups
from typing import Dict, List

def build_section_cards(tablas: list[str], labels: dict[str,str], base_path: str, cols_per_row: dict = None):
    """
    Genera una lista de dbc.Col(dbc.Card) para una sección:
      - tablas: lista de nombres de tabla en la base.
      - labels: map tabla->título descriptivo.
      - base_path: ruta raíz de la sección, p.ej. "/cuentas-nacionales"
      - cols_per_row: opcional dict de breakpoints, p.ej. {"xs":12,"sm":6,"md":4}
    """
    if cols_per_row is None:
        cols_per_row = {"xs":12, "sm":6, "md":4, "lg":3}
    cards = []
    for tbl in tablas:
        link = f"{base_path}/{tbl.replace('_','-')}"
        cards.append(
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H5(labels[tbl], className="card-title"),
                        html.P(f"({tbl})", className="text-muted small"),
                        dbc.Button("Ver detalle ➔", href=link, color="primary", size="sm", className="mt-2"),
                    ])
                ],
                class_name="h-100 card-hover shadow-sm",
                style={"cursor":"pointer"}),
                **cols_per_row,
                className="mb-4"
            )
        )
    return dbc.Row(cards, class_name="g-4")

def build_breadcrumb(
    crumbs: list[dict],
    status: str,
    badge_success_marker: str = "✅"
) -> dbc.Row:
    """
    Construye la fila de breadcrumb + badge de estado.

    Parameters
    ----------
    crumbs : list of dict
        Cada dict debe tener:
          - 'label': texto a mostrar.
          - opcionalmente 'href' o 'active': para el breadcrumb.
    status : str
        Texto del badge (p.ej. "✅ OK" o "⚠️ Revisar").
    badge_success_marker : str
        Si 'status' contiene este marcador, usa bg-success; 
        si no, bg-danger.

    Returns
    -------
    dbc.Row
    """
    bc = dbc.Breadcrumb(items=crumbs)
    badge_class = "bg-success" if badge_success_marker in status else "bg-danger"
    badge = html.Span(status, className=f"badge {badge_class}")
    return dbc.Row(
        [
            dbc.Col(bc, md=8),
            dbc.Col(badge, md=4, style={"textAlign": "right"}),
        ],
        align="center",
        className="mb-1",
    )


#-------------
#Header
#-------------
def build_metadata_panel(meta: dict) -> dbc.Card:
    rows = [
        dbc.Row(
            [dbc.Col(html.Small(f"{k}:"), width=4),
             dbc.Col(html.Small(v),       width=8)],
            className="mb-1"
        )
        for k, v in meta.items()
    ]
    return dbc.Card(dbc.CardBody(rows), className="mt-2")
def build_header(
    title: str,
    desc: str,
    metadata: dict,
    toggle_id: str = "btn-toggle-meta",
    collapse_id: str = "meta-panel"
) -> html.Div:
    """
    Construye el bloque de título, subtítulo y metadatos colapsables.

    Parameters
    ----------
    title : str
        Título principal de la tabla (p.ej. "PIB por ramas de actividad").
    desc : str
        Subtítulo o descripción breve.
    metadata : dict
        Diccionario de metadatos que será pasado a build_metadata_panel().
    toggle_id : str
        ID para el botón que abre/cierra el panel.
    collapse_id : str
        ID para el componente Collapse del panel.

    Returns
    -------
    html.Div
    """

    return html.Div(
        [
            html.H2(title),
            html.P(desc),
            dbc.Button(
                "Mostrar detalles de la tabla",
                id=toggle_id,
                color="link",
                className="p-0 mb-1",
            ),
            dbc.Collapse(
                build_metadata_panel(metadata),
                id=collapse_id,
                is_open=False,
            ),
        ],
        className="mb-3",
    )


def build_image_gallery_card(
    groups: Dict[str, List[str]],
    table_id: str,
    title: str = "Galería de imágenes",
    initially_open: bool = False,
    toggle_id: str = "btn-toggle-img",
    collapse_id: str = "img-panel",
) -> dbc.Card:
    """
    Devuelve una Card con Header (título + botón mostrar/ocultar) y un Collapse
    que contiene Tabs con las imágenes. Cada tab renderiza la lista de imágenes
    del grupo; cada imagen tiene un botón 'Descargar'.

    Parámetros
    ----------
    groups : dict[str, list[str]]
        Mapa { etiqueta_grupo: [ "img1.png", "img2.png", ... ] }.
        Suele tener claves como "Serie completa" y/o "Crisis".
    table_id : str
        Id de la tabla para resolver la ruta en /assets/<folder>/<table_id>/<img>.
    title : str
        Título a mostrar en el CardHeader.
    initially_open : bool
        Si True, el Collapse arranca abierto.
    toggle_id : str
        ID del botón que abre/cierra el Collapse.
    collapse_id : str
        ID del Collapse.

    Retorna
    -------
    dbc.Card
    """

    def _infer_folder(label: str) -> str:
        """Mapea la etiqueta del grupo a la carpeta dentro de assets/."""
        low = label.strip().lower()
        if "serie" in low and "completa" in low:
            return "serie_completa"
        if "crisis" in low:
            return "crisis"
        # fallback: slugify simple
        return low.replace(" ", "_")

    # Construir Tabs (una por grupo)
    tabs = []
    for label, imgs in groups.items():
        if not imgs:
            content = html.P("No hay imágenes disponibles.", className="text-muted")
        else:
            rows = []
            folder = _infer_folder(label)
            for img in imgs:
                asset_path = f"{folder}/{table_id}/{img}"  # relativo a assets/
                src = dash.get_asset_url(asset_path)
                rows.append(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(
                                    src=src,
                                    alt=f"{label} – {img}",
                                    className="img-fluid rounded shadow-sm mb-2",
                                ),
                                width=12,
                            ),
                            dbc.Col(
                                html.A(
                                    "Descargar",
                                    href=src,
                                    download=img,
                                    target="_blank",
                                    className="btn btn-primary mb-4",
                                ),
                                width="auto",
                            ),
                        ],
                        className="align-items-center",
                    )
                )
            content = html.Div(rows)
        tabs.append(dbc.Tab(content, label=label))

    tabs_component = dbc.Tabs(tabs, id=f"{collapse_id}-tabs", className="mb-0")

    return dbc.Card(
        [
            dbc.CardHeader(
                dbc.Row(
                    [
                        dbc.Col(html.Strong(title), align="center"),
                        dbc.Col(
                            dbc.Button(
                                "Mostrar/Ocultar",
                                id=toggle_id,
                                color="link",
                                className="p-0",
                            ),
                            width="auto",
                            style={"textAlign": "right"},
                        ),
                    ],
                    align="center",
                )
            ),
            dbc.Collapse(
                dbc.CardBody(tabs_component),
                id=collapse_id,
                is_open=initially_open,
            ),
        ],
        className="my-4 shadow-sm",
    )

def build_data_table(
    df,
    table_id: str,
    table_styles: dict,
    page_size: int = 10
):
    """
    Genera un componente DataTable estandarizado para cualquier tabla.

    Parámetros
    ----------
    df : pandas.DataFrame
        DataFrame ya indexado (con índice significativo, p.ej. 'año').
    table_id : str
        Identificador para el componente (se usa en id="{table_id}-table").
    table_styles : dict
        Diccionario con estilos base: style_table, style_cell, style_header.
    page_size : int, opcional
        Número de filas por página (por defecto 10).

    Retorna
    -------
    dash_table.DataTable
    """
    # Preparar datos y columnas
    data = df.reset_index().to_dict("records") if not df.empty else []
    columns = (
        [{"name": c, "id": c} for c in df.reset_index().columns]
        if not df.empty else []
    )
    # Tooltips como texto plano
    tooltip_data = (
        [
            {c: {"value": str(v), "type": "text"} for c, v in row.items()}
            for row in df.reset_index().to_dict("records")
        ]
        if not df.empty else []
    )

    return dash_table.DataTable(
        id=f"{table_id}-table",
        data=data,
        columns=columns,
        page_size=page_size,
        page_action="native",
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        export_format="csv",
        export_headers="display",
        virtualization=True,
        fixed_rows={"headers": True},
        tooltip_data=tooltip_data,
        tooltip_duration=None,
        # Estilos personalizados
        **table_styles,
        # Style_conditional para filas y celdas específicas
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "#f1f3f5"},
        ],
        style_cell_conditional=[
            {"if": {"column_id": df.index.name or "año"}, "textAlign": "left", "fontWeight": "600"},
        ],
    )