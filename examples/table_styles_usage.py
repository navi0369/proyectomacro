# Ejemplo de uso de estilos de tabla centralizados
"""
Este archivo muestra diferentes formas de usar los estilos de tabla centralizados
"""

from proyectomacro.page_utils import get_table_styles, build_data_table

# ──────────────────────────────────────────────────────────────────────
# CASO 1: Usar estilos predeterminados (más común)
# ──────────────────────────────────────────────────────────────────────

# Opción A: No pasar table_styles (recomendado para la mayoría de casos)
build_data_table(df, TABLE_ID, page_size=10)

# Opción B: Obtener explícitamente los estilos predeterminados
default_styles = get_table_styles()
build_data_table(df, TABLE_ID, table_styles=default_styles, page_size=10)

# ──────────────────────────────────────────────────────────────────────
# CASO 2: Personalizar estilos específicos
# ──────────────────────────────────────────────────────────────────────

# Cambiar solo el color del header
custom_styles = get_table_styles({
    "style_header": {
        "backgroundColor": "#28a745",  # Verde en lugar de azul
        "fontWeight": "bold",
        "color": "white",
    }
})
build_data_table(df, TABLE_ID, table_styles=custom_styles)

# Cambiar solo el tamaño de fuente
custom_styles = get_table_styles({
    "style_cell": {
        "fontSize": "16px"  # Fuente más grande
    }
})
build_data_table(df, TABLE_ID, table_styles=custom_styles)

# Personalización múltiple
custom_styles = get_table_styles({
    "style_header": {
        "backgroundColor": "#dc3545",  # Rojo
        "color": "white"
    },
    "style_cell": {
        "fontSize": "12px",
        "padding": "12px"
    }
})
build_data_table(df, TABLE_ID, table_styles=custom_styles)

# ──────────────────────────────────────────────────────────────────────
# CASO 3: Estilos completamente personalizados
# ──────────────────────────────────────────────────────────────────────

completely_custom = {
    "style_table": {"overflowX": "auto", "border": "1px solid #ddd"},
    "style_cell": {
        "textAlign": "left",
        "padding": "15px",
        "fontFamily": "Georgia, serif",
        "fontSize": "14px",
        "border": "1px solid #eee"
    },
    "style_header": {
        "backgroundColor": "#6c757d",
        "fontWeight": "normal",
        "color": "white",
        "textTransform": "uppercase"
    },
}
build_data_table(df, TABLE_ID, table_styles=completely_custom)

# ──────────────────────────────────────────────────────────────────────
# VENTAJAS DEL SISTEMA CENTRALIZADO
# ──────────────────────────────────────────────────────────────────────

"""
✅ ANTES (problemático):
- Cada página tenía que definir table_styles manualmente
- Código duplicado en 15+ archivos
- Inconsistencias entre páginas
- Difícil cambiar estilos globalmente

✅ DESPUÉS (mejorado):
- Estilos centralizados en page_utils.py
- Una sola fuente de verdad
- Consistencia automática
- Fácil personalización cuando sea necesario
- Cambios globales desde un solo lugar

📝 RECOMENDACIONES:
1. Usar build_data_table(df, TABLE_ID) sin table_styles para el 90% de casos
2. Personalizar solo cuando sea necesario para casos específicos
3. Documentar por qué se personalizan los estilos en casos especiales
"""
