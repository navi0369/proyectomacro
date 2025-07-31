# page_factory.py
from pathlib import Path
from typing import Dict, List

import dash_bootstrap_components as dbc
from dash import html, dash_table, get_asset_url
from extract_data import load_validated_tables, list_table_images


def build_table_page(
    table_id: str,
    title: str,
    description: str = "",
    path_prefix: str = "",
) -> html.Div:
    """
    Devuelve un `dbc.Container` listo para usar como layout de página Dash.

    Args
    ----
    table_id      : nombre real de la tabla en DB  (p.ej. 'pib_ramas')
    title         : título mostrado al usuario     (p.ej. 'PIB por ramas')
    description   : párrafo opcional bajo el título
    path_prefix   : subcarpeta dentro de /assets   (e.g. 'serie_completa')
    """
    # 1. Cargar datos validados
    dfs = load_validated_tables()
    df = dfs[table_id].reset_index()
    columns = [{"name": c, "id": c} for c in df.columns]

    # 2. Agrupar imágenes
    imgs = list_table_images(table_id)
    print(f"Imágenes encontradas para {table_id}: {imgs}")
    groups: Dict[str, List[str]] = {
        "Serie completa": [f for f in imgs if "_full" in f],
        "Sub-series":     [f for f in imgs if "_full" not in f],
    }

    # 3. Tabs dinámicos
    tabs = []
    for label, files in groups.items():
        if files:
            cards = [
                dbc.Col(
                    html.Img(
                        src=get_asset_url(f"{path_prefix}/{table_id}/{png}")
                        if path_prefix else
                        get_asset_url(f"{table_id}/{png}"),
                        className="img-fluid",
                        style={"borderRadius": "4px"},
                    ),
                    xs=12, sm=6, md=4, className="mb-4",
                )
                for png in files
            ]
            content = dbc.Row(cards, className="g-4")
        else:
            content = html.P(
                "No hay gráficos en esta categoría.",
                className="text-muted fst-italic",
            )
        tabs.append(dbc.Tab(content, label=label, tab_id=label))

    tab_component = (
        dbc.Tabs(
            tabs,
            id=f"tabs-{table_id}",
            active_tab="Serie completa"
            if groups["Serie completa"]
            else (tabs[0].tab_id if tabs else None),
        )
        if tabs
        else html.P("No hay gráficos disponibles.", className="text-muted")
    )

    # 4. Componer layout
    return dbc.Container(
        [
            html.H3(title, className="mb-2"),
            html.P(description, className="text-muted") if description else None,
            tab_component,
            dbc.Row(
                dbc.Col(
                    dash_table.DataTable(
                        data=df.to_dict("records"),
                        columns=columns,
                        page_size=10,
                        style_table={"overflowX": "auto"},
                        style_header={
                            "backgroundColor": "#f8f9fa",
                            "fontWeight": "bold",
                        },
                        style_cell={
                            "padding": "6px",
                            "textAlign": "left",
                            "whiteSpace": "normal",
                        },
                    ),
                    xs=12,
                    className="mt-4",
                )
            ),
        ],
        fluid=True,
        className="p-4",
    )
