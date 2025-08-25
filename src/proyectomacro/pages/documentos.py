# src/proyectomacro/pages/documentos.py
import os
from datetime import datetime
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from pathlib import Path

# Registro de la página
dash.register_page(__name__, name="Documentos", path="/documentos")

# Directorio de documentos
DOCUMENTS_DIR = Path(__file__).parent.parent.parent.parent / "reports" / "documents"

def get_file_icon(file_extension):
    """Devuelve el icono apropiado según la extensión del archivo"""
    icons = {
        '.pdf': '📄',
        '.csv': '📊',
        '.xlsx': '📊',
        '.xls': '📊',
        '.docx': '📝',
        '.doc': '📝',
        '.md': '📝',
        '.txt': '📝',
        '.tex': '📝',
        '.png': '🖼️',
        '.jpg': '🖼️',
        '.jpeg': '🖼️',
        '.gif': '🖼️',
        '.zip': '🗜️',
        '.rar': '🗜️',
    }
    return icons.get(file_extension.lower(), '📁')

def get_file_size(filepath):
    """Devuelve el tamaño del archivo en formato legible"""
    try:
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except:
        return "N/A"

def get_file_modified_date(filepath):
    """Devuelve la fecha de modificación del archivo"""
    try:
        timestamp = os.path.getmtime(filepath)
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
    except:
        return "N/A"

def scan_documents_directory():
    """Escanea el directorio de documentos y devuelve una lista de archivos"""
    documents = []
    
    if not DOCUMENTS_DIR.exists():
        return documents
    
    for root, dirs, files in os.walk(DOCUMENTS_DIR):
        for file in files:
            filepath = Path(root) / file
            relative_path = filepath.relative_to(DOCUMENTS_DIR)
            
            file_info = {
                'name': file,
                'path': str(relative_path),
                'full_path': str(filepath),
                'extension': filepath.suffix,
                'icon': get_file_icon(filepath.suffix),
                'size': get_file_size(filepath),
                'modified': get_file_modified_date(filepath),
                'category': get_file_category(filepath.suffix)
            }
            documents.append(file_info)
    
    return sorted(documents, key=lambda x: x['name'])

def get_file_category(extension):
    """Categoriza los archivos por tipo"""
    categories = {
        'Documentos': ['.pdf', '.docx', '.doc', '.txt', '.md', '.tex'],
        'Hojas de Cálculo': ['.xlsx', '.xls', '.csv'],
        'Imágenes': ['.png', '.jpg', '.jpeg', '.gif'],
        'Archivos Comprimidos': ['.zip', '.rar'],
    }
    
    for category, extensions in categories.items():
        if extension.lower() in extensions:
            return category
    return 'Otros'

def create_file_card(file_info):
    """Crea una tarjeta para mostrar información del archivo"""
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Span(file_info['icon'], style={'fontSize': '2rem', 'marginRight': '10px'}),
                html.H5(file_info['name'], className="card-title", style={'display': 'inline-block'})
            ]),
            html.P(f"Categoría: {file_info['category']}", className="card-text"),
            html.P(f"Tamaño: {file_info['size']}", className="card-text"),
            html.P(f"Modificado: {file_info['modified']}", className="card-text"),
            html.P(f"Ruta: {file_info['path']}", className="card-text text-muted", style={'fontSize': '0.8rem'}),
            dbc.Button(
                "Abrir documento",
                color="primary",
                size="sm",
                href=f"/reports/documents/{file_info['path']}",
                target="_blank",
                external_link=True
            )
        ])
    ], style={'margin': '10px', 'height': '300px'})

def create_documents_layout():
    """Crea el layout principal de la página de documentos"""
    documents = scan_documents_directory()
    
    # Agrupa documentos por categoría
    categories = {}
    for doc in documents:
        category = doc['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(doc)
    
    # Estadísticas generales
    total_files = len(documents)
    total_size = sum([os.path.getsize(doc['full_path']) if os.path.exists(doc['full_path']) else 0 for doc in documents])
    total_size_str = get_file_size_from_bytes(total_size)
    
    # Controles de filtrado
    category_options = [{"label": "Todas las categorías", "value": "all"}]
    category_options.extend([{"label": cat, "value": cat} for cat in categories.keys()])
    
    filter_controls = dbc.Row([
        dbc.Col([
            html.Label("Filtrar por categoría:", className="form-label"),
            dcc.Dropdown(
                id="category-filter",
                options=category_options,
                value="all",
                clearable=False
            )
        ], width=4),
        dbc.Col([
            html.Label("Buscar archivo:", className="form-label"),
            dcc.Input(
                id="search-input",
                type="text",
                placeholder="Escriba el nombre del archivo...",
                className="form-control"
            )
        ], width=4),
        dbc.Col([
            html.Label("Ordenar por:", className="form-label"),
            dcc.Dropdown(
                id="sort-dropdown",
                options=[
                    {"label": "Nombre", "value": "name"},
                    {"label": "Fecha de modificación", "value": "modified"},
                    {"label": "Tamaño", "value": "size"},
                    {"label": "Tipo", "value": "extension"}
                ],
                value="name",
                clearable=False
            )
        ], width=4)
    ], className="mb-4")
    
    return html.Div([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("📚 Centro de Documentos", className="display-4"),
                html.P("Acceso centralizado a todos los documentos del proyecto", className="lead"),
                html.Hr()
            ], width=12)
        ]),
        
        # Estadísticas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{total_files}", className="card-title text-primary"),
                        html.P("Total de archivos", className="card-text")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{len(categories)}", className="card-title text-success"),
                        html.P("Categorías", className="card-text")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(total_size_str, className="card-title text-info"),
                        html.P("Tamaño total", className="card-text")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📁", className="card-title text-warning"),
                        html.P("Directorio", className="card-text"),
                        html.Small("reports/documents", className="text-muted")
                    ])
                ])
            ], width=3)
        ], className="mb-4"),
        
        # Controles de filtrado
        filter_controls,
        
        # Contenedor de documentos
        html.Div(id="documents-container"),
        
        # Información adicional
        dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.H4("💡 Información", className="alert-heading"),
                    html.P("Los documentos se organizan automáticamente por categorías. "
                          "Utilice los filtros para encontrar archivos específicos."),
                    html.Hr(),
                    html.P("Para agregar nuevos documentos, colóquelos en el directorio: ",
                          className="mb-0"),
                    html.Code("reports/documents/", className="ms-2")
                ], color="info", className="mt-4")
            ], width=12)
        ])
    ], className="p-4")

def get_file_size_from_bytes(size_bytes):
    """Convierte bytes a formato legible"""
    if size_bytes == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

# Layout principal
layout = create_documents_layout()

# Callback para filtrar y ordenar documentos
@callback(
    Output("documents-container", "children"),
    [Input("category-filter", "value"),
     Input("search-input", "value"),
     Input("sort-dropdown", "value")]
)
def update_documents_display(category_filter, search_term, sort_by):
    """Actualiza la visualización de documentos según los filtros"""
    documents = scan_documents_directory()
    
    # Filtrar por categoría
    if category_filter and category_filter != "all":
        documents = [doc for doc in documents if doc['category'] == category_filter]
    
    # Filtrar por término de búsqueda
    if search_term:
        search_term = search_term.lower()
        documents = [doc for doc in documents if search_term in doc['name'].lower()]
    
    # Ordenar
    if sort_by == "name":
        documents = sorted(documents, key=lambda x: x['name'].lower())
    elif sort_by == "modified":
        documents = sorted(documents, key=lambda x: x['modified'], reverse=True)
    elif sort_by == "size":
        documents = sorted(documents, key=lambda x: os.path.getsize(x['full_path']) if os.path.exists(x['full_path']) else 0, reverse=True)
    elif sort_by == "extension":
        documents = sorted(documents, key=lambda x: x['extension'])
    
    if not documents:
        return dbc.Alert(
            "No se encontraron documentos con los filtros aplicados.",
            color="warning",
            className="text-center"
        )
    
    # Crear tarjetas de documentos
    cards = []
    for doc in documents:
        cards.append(
            dbc.Col(create_file_card(doc), width=12, md=6, lg=4, xl=3)
        )
    
    return dbc.Row(cards)
