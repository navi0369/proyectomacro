# test_config_loader.py
"""
Script de prueba para verificar que el cargador de configuración funciona correctamente
"""
import sys
from pathlib import Path

# Agregar src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

from proyectomacro.config_loader import config_loader, get_table_metadata, get_table_config

def test_config_loader():
    """Prueba las funciones del cargador de configuración"""
    
    print("🧪 Probando el cargador de configuración...")
    print("=" * 50)
    
    # 1. Probar obtener todas las secciones
    print("1. Secciones disponibles:")
    sections = config_loader.get_sections()
    for section_name in sections.keys():
        print(f"   - {section_name}")
    print()
    
    # 2. Probar obtener configuración de una tabla específica
    print("2. Configuración de la tabla 'pib_ramas':")
    pib_ramas_config = get_table_config("pib_ramas")
    if pib_ramas_config:
        print(f"   Tabla: {pib_ramas_config.get('tabla')}")
        print(f"   Label: {pib_ramas_config.get('label')}")
        print(f"   Tiene metadatos: {'metadata' in pib_ramas_config}")
    else:
        print("   ❌ No se encontró la configuración")
    print()
    
    # 3. Probar obtener metadatos específicos
    print("3. Metadatos de la tabla 'pib_ramas':")
    pib_ramas_metadata = get_table_metadata("pib_ramas")
    if pib_ramas_metadata:
        print(f"   Nombre descriptivo: {pib_ramas_metadata.get('nombre_descriptivo')}")
        print(f"   Período: {pib_ramas_metadata.get('periodo')}")
        print(f"   Fuentes: {len(pib_ramas_metadata.get('fuentes', []))} fuente(s)")
        print(f"   Unidades: {len(pib_ramas_metadata.get('unidades', {}))} unidad(es)")
        print(f"   Notas: {len(pib_ramas_metadata.get('notas', []))} nota(s)")
    else:
        print("   ❌ No se encontraron metadatos")
    print()
    
    # 4. Probar conversión a formato para build_metadata_panel
    print("4. Conversión a formato estándar:")
    if pib_ramas_metadata:
        formatted = {
            "Nombre descriptivo": pib_ramas_metadata.get("nombre_descriptivo", ""),
            "Período": pib_ramas_metadata.get("periodo", ""),
            "Unidad": pib_ramas_metadata.get("unidades", {}),
            "Fuente": pib_ramas_metadata.get("fuentes", []),
            "Estado de validación": "✅ OK",
        }
        if pib_ramas_metadata.get("notas"):
            formatted["Notas"] = pib_ramas_metadata["notas"]
        
        for key, value in formatted.items():
            print(f"   {key}: {value}")
    print()
    
    # 5. Probar con tabla que no existe
    print("5. Probando con tabla inexistente:")
    nonexistent = get_table_metadata("tabla_inexistente")
    if nonexistent is None:
        print("   ✅ Correctamente retorna None para tabla inexistente")
    else:
        print("   ❌ Error: debería retornar None")
    
    print("=" * 50)
    print("🎉 Pruebas completadas!")

if __name__ == "__main__":
    test_config_loader()
