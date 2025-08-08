# src/proyectomacro/config_loader.py
"""
Módulo para cargar y gestionar la configuración de páginas y metadatos desde pages.yml
"""
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Cargador de configuración para páginas y metadatos"""
    
    def __init__(self, config_path: Optional[Path] = None):
        if config_path is None:
            # Buscar pages.yml en la carpeta config del proyecto
            config_path = Path(__file__).parent / "config" / "pages.yml"
        
        self.config_path = config_path
        self._config = None
        self._load_config()
    
    def _load_config(self):
        """Carga el archivo YAML de configuración"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
            logger.info(f"Configuración cargada desde {self.config_path}")
        except FileNotFoundError:
            logger.error(f"No se encontró el archivo de configuración: {self.config_path}")
            self._config = {"secciones": {}}
        except yaml.YAMLError as e:
            logger.error(f"Error al parsear YAML: {e}")
            self._config = {"secciones": {}}
    
    def get_sections(self) -> Dict[str, Any]:
        """Retorna todas las secciones definidas"""
        return self._config.get("secciones", {})
    
    def get_section(self, section_key: str) -> Optional[Dict[str, Any]]:
        """Retorna una sección específica"""
        return self.get_sections().get(section_key)
    
    def get_table_config(self, section_key: str, table_key: str) -> Optional[Dict[str, Any]]:
        """Retorna la configuración completa de una tabla específica"""
        section = self.get_section(section_key)
        if not section:
            return None
        
        tables = section.get("tablas", {})
        return tables.get(table_key)
    
    def get_table_metadata(self, section_key: str, table_key: str) -> Optional[Dict[str, Any]]:
        """Retorna solo los metadatos de una tabla específica"""
        table_config = self.get_table_config(section_key, table_key)
        if not table_config:
            return None
        
        return table_config.get("metadata")
    
    def find_table_by_id(self, table_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca una tabla por su ID en todas las secciones
        Retorna: {"section_key": str, "table_key": str, "config": dict}
        """
        for section_key, section_data in self.get_sections().items():
            tables = section_data.get("tablas", {})
            for table_key, table_config in tables.items():
                if table_config.get("tabla") == table_id:
                    return {
                        "section_key": section_key,
                        "table_key": table_key,
                        "config": table_config
                    }
        return None
    
    def get_metadata_for_table_id(self, table_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca y retorna los metadatos de una tabla por su ID
        """
        table_info = self.find_table_by_id(table_id)
        if not table_info:
            return None
        
        return table_info["config"].get("metadata")

# Instancia global del cargador de configuración
config_loader = ConfigLoader()

# Funciones de conveniencia
def get_table_metadata(table_id: str) -> Optional[Dict[str, Any]]:
    """Función de conveniencia para obtener metadatos de una tabla"""
    return config_loader.get_metadata_for_table_id(table_id)

def get_table_config(table_id: str) -> Optional[Dict[str, Any]]:
    """Función de conveniencia para obtener la configuración completa de una tabla"""
    table_info = config_loader.find_table_by_id(table_id)
    return table_info["config"] if table_info else None

def get_all_sections() -> Dict[str, Any]:
    """Función de conveniencia para obtener todas las secciones"""
    return config_loader.get_sections()
