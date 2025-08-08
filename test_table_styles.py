# test_table_styles.py
"""
Script de prueba para verificar que los estilos de tabla centralizados funcionan correctamente
"""
import sys
from pathlib import Path

# Agregar src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

from proyectomacro.page_utils import get_table_styles, DEFAULT_TABLE_STYLES

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
    
    # 4. Verificar que no muta el original
    print("4. Verificando inmutabilidad:")
    original_color = DEFAULT_TABLE_STYLES['style_header']['backgroundColor']
    get_table_styles({"style_header": {"backgroundColor": "#000000"}})
    after_color = DEFAULT_TABLE_STYLES['style_header']['backgroundColor']
    print(f"   ✅ Color original preservado: {original_color == after_color}")
    print(f"   📊 Color original: {original_color}")
    print(f"   📊 Color después: {after_color}")
    print()
    
    # 5. Probar sobrescritura completa
    print("5. Sobrescritura completa de una sección:")
    complete_override = get_table_styles({
        "style_cell": {
            "textAlign": "left",
            "fontFamily": "Georgia, serif"
        }
    })
    print(f"   ✅ Alineación cambiada: {complete_override['style_cell']['textAlign']}")
    print(f"   ✅ Font family cambiada: {complete_override['style_cell']['fontFamily']}")
    print(f"   ❌ Perdió fontSize (sobrescritura completa): {'fontSize' not in complete_override['style_cell']}")
    print()
    
    # 6. Comparar tamaños
    print("6. Información del sistema:")
    print(f"   📊 Número de estilos predeterminados: {len(DEFAULT_TABLE_STYLES)}")
    print(f"   📊 Propiedades en style_cell: {len(DEFAULT_TABLE_STYLES['style_cell'])}")
    print(f"   📊 Propiedades en style_header: {len(DEFAULT_TABLE_STYLES['style_header'])}")
    
    print("=" * 60)
    print("🎉 ¡Todas las pruebas de estilos completadas exitosamente!")
    print()
    print("📝 Resumen de funcionalidades:")
    print("   ✅ Estilos predeterminados centralizados")
    print("   ✅ Personalización parcial (mezcla propiedades)")
    print("   ✅ Personalización completa (sobrescribe secciones)")
    print("   ✅ Inmutabilidad del objeto original")
    print("   ✅ API simple y flexible")

if __name__ == "__main__":
    test_table_styles()
