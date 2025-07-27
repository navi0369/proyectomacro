"""Definición y carga de reglas de validación para cada tabla."""

from dataclasses import dataclass, field
from typing import List
from pathlib import Path
import yaml
from typing import Dict

@dataclass
class TableRule:
    # Nombre de la columna índice (debe ser “año” o Datetime)
    index: str = "año"

    # Columnas de datos numéricos a validar
    value_cols: List[str] = field(default_factory=lambda: ["valor"])

    # Validaciones estructurales
    check_index_is_year: bool = True  # 1. Índice debe ser año
    check_unique_index: bool = True   # 2. Índices no repetidos
    check_monotonic_index: bool = True  # 3. Índice cronológico
    check_required_columns: bool = True  # 4. Columnas requeridas

    # Validaciones de contenido
    check_no_nulls: bool = True  # 5. No hay NaN/Null/vacíos
    check_numeric: bool = True  # 6. Todos los datos son numéricos
    check_gaps: bool = True  # 7. Huecos en la secuencia
    check_outliers: bool = False  # 8. Saltos atípicos (>4σ)

    # busca un archivo 'rules.yml' al lado de este módulo
_YAML_PATH = Path(__file__).with_suffix(".yml")

def load_rules() -> Dict[str, TableRule]:
    """Carga las reglas desde ``validation/rules.yml``.

    Devuelve ``{nombre_tabla: TableRule}`` y usa valores por defecto cuando
    faltan campos. Si no existe el YAML se devuelve un dict vacío.
    """
    if not _YAML_PATH.exists():
        return {}

    raw = yaml.safe_load(_YAML_PATH.read_text()) or {}
    rules: Dict[str, TableRule] = {}
    for table_name, params in raw.items():
        # ``params`` mapea keys a los atributos de ``TableRule``
        rules[table_name] = TableRule(**params)
    return rules

