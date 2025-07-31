#src/proyectomacro/extract_data.py
import os
from validation.validate_all import validate_database
import sqlite3
import pandas as pd
from func_auxiliares.config import ASSETS_DIR, DB_PATH
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)
def load_validated_tables(db_path: str = str(DB_PATH)) -> dict[str, pd.DataFrame]:
    # 1.1. Ejecutar la validación y obtener el DataFrame de resultados
    results = validate_database(db_path)

    # 1.2. Filtrar sólo las tablas con status "OK"
    valid_tables = results.loc[results.status == "OK", "table"].tolist()

    # 1.3. Conectar a la base y leer cada tabla validada en un DataFrame
    conn = sqlite3.connect(db_path, uri=True)
    dfs: dict[str, pd.DataFrame] = {}
    for tbl in valid_tables:
        try:
            df = pd.read_sql(f"SELECT * FROM {tbl}", conn, index_col="año")
            num_cols = df.select_dtypes(include="number").columns
            df[num_cols] = df[num_cols].round(2)
            dfs[tbl] = df
        except Exception as e:
            # log warning, no rompe toda la carga
            logger.warning("No se pudo cargar tabla %s: %s", tbl, e)
    conn.close()

    return dfs


def list_table_image_groups(table_id: str) -> Dict[str, List[str]]:
    """
    Busca dentro de assets/ las subcarpetas relevantes para la tabla y devuelve
    un dict {etiqueta: [nombres de png]}.

    Convenciones:
      - assets/serie_completa/<table_id>/ → "Serie completa"
      - assets/crisis/<table_id>/         → "Crisis"
    """
    groups: Dict[str, List[str]] = {
        "Serie completa": [],
        "Crisis": [],
    }

    mapping = {
        "Serie completa": ASSETS_DIR / "serie_completa" / table_id,
        "Crisis": ASSETS_DIR / "crisis" / table_id,
    }

    for label, folder in mapping.items():
        if folder.exists() and folder.is_dir():
            imgs = sorted([
                f for f in os.listdir(folder)
                if f.lower().endswith((".png", ".jpg", ".jpeg"))
            ])
            groups[label] = imgs

    return groups

if __name__ == "__main__":
    data_dict = load_validated_tables()
    # Ejemplo: listar tablas cargadas
    print("Tablas cargadas:", list(data_dict.keys()))
