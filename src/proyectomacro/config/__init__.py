# src/proyectomacro/config/__init__.py
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "pages.yml"

def load_pages_config() -> dict:
    """
    Devuelve el dict de secciones definido en pages.yml:
    { "cuentas_nacionales": { name, path, tablas: { ... } }, ... }
    """
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)["secciones"]