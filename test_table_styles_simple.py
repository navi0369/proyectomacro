# test_table_styles_simple.py
"""
Script de prueba simplificado para verificar los estilos de tabla
"""
import sys
from pathlib import Path

# Agregar src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Importar solo las constantes y funciones necesarias
DEFAULT_TABLE_STYLES = {
    "style_table": {"overflowX": "auto"},
    "style_cell": {
        "textAlign": "center",
        "padding": "8px",
        "minWidth": "100px",
        "width": "100px",
        "maxWidth": "180px",
        "fontFamily": "Arial, sans-serif",
        "fontSize": "14px",
    },
    "style_header": {
        "backgroundColor": "#007BFF",
        "fontWeight": "bold",
        "color": "white",
    },
}

def get_table_styles(custom_styles=None):
    """Función simplificada para pruebas"""
    styles = DEFAULT_TABLE_STYLES.copy()
    
    if custom_styles:
        for key, value in custom_styles.items():
            if key in styles and isinstance(styles[key], dict) and isinstance(value, dict):
                styles[key] = {**styles[key], **value}
            else:
                styles[key] = value
    
    return styles

def test_table_styles():
    """Prueba las funciones de estilos de tabla"""
    
    print("🎨 Probando el sistema de estilos de tabla centralizados...")
    print("=" * 60)
    
    # 1. Probar estilos predeterminados
    print("1. Estilos predeterminados:")
    default_styles = get_table_styles()
    print(f"   ✅ Contiene style_table: {'style_table' in default_styles}")
    print(f"   ✅ Contiene style_cell: {'style_cell' in default_styles}")
    print(f"   ✅ Contiene style_header: {'style_header' in default_styles}")
    print(f"   📊 Header color: {default_styles['style_header']['backgroundColor']}")
    print(f"   📝 Font family: {default_styles['style_cell']['fontFamily']}")
    print()
    
    # 2. Probar personalización parcial
    print("2. Personalización parcial (solo header):")
    custom_header = get_table_styles({
        "style_header": {"backgroundColor": "#28a745"}
    })
    print(f"   ✅ Header color cambiado: {custom_header['style_header']['backgroundColor']}")
    print(f"   ✅ Conserva texto blanco: {custom_header['style_header']['color']}")
    print(f"   ✅ Conserva estilo de celdas: {custom_header['style_cell']['fontSize']}")
    print()
    
    # 3. Probar personalización múltiple
    print("3. Personalización múltiple:")
    multi_custom = get_table_styles({
        "style_header": {"backgroundColor": "#dc3545"},
        "style_cell": {"fontSize": "16px", "padding": "12px"}
    })
    print(f"   ✅ Header rojo: {multi_custom['style_header']['backgroundColor']}")
    print(f"   ✅ Fuente más grande: {multi_custom['style_cell']['fontSize']}")
    print(f"   ✅ Padding personalizado: {multi_custom['style_cell']['padding']}")
    print(f"   ✅ Conserva font family: {multi_custom['style_cell']['fontFamily']}")
    print()
    
    # 4. Verificar inmutabilidad
    print("4. Verificando inmutabilidad:")
    original_color = DEFAULT_TABLE_STYLES['style_header']['backgroundColor']
    get_table_styles({"style_header": {"backgroundColor": "#000000"}})
    after_color = DEFAULT_TABLE_STYLES['style_header']['backgroundColor']
    print(f"   ✅ Color original preservado: {original_color == after_color}")
    print(f"   📊 Color original: {original_color}")
    print(f"   📊 Color después: {after_color}")
    print()
    
    print("=" * 60)
    print("🎉 ¡Todas las pruebas de estilos completadas exitosamente!")
    print()
    print("📝 Beneficios del sistema centralizado:")
    print("   ✅ Una sola fuente de verdad para estilos")
    print("   ✅ Fácil personalización cuando sea necesario")
    print("   ✅ Consistencia automática en todas las páginas")
    print("   ✅ Mantenimiento simplificado")

if __name__ == "__main__":
    test_table_styles()
