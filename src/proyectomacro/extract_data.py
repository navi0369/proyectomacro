#src/proyectomacro/extract_data.py
from validation.validate_all import validate_database
from config import DB_PATH
import sqlite3
import pandas as pd

def load_validated_tables(db_path: str = DB_PATH) -> dict[str, pd.DataFrame]:
    # 1.1. Ejecutar la validación y obtener el DataFrame de resultados
    results = validate_database(db_path)

    # 1.2. Filtrar sólo las tablas con status "OK"
    valid_tables = results.loc[results.status == "OK", "table"].tolist()

    # 1.3. Conectar a la base y leer cada tabla validada en un DataFrame
    conn = sqlite3.connect(db_path, uri=True)
    dfs: dict[str, pd.DataFrame] = {}
    for tbl in valid_tables:
        # asumiendo que todas usan 'año' como índice
        dfs[tbl] = pd.read_sql(f"SELECT * FROM {tbl}", conn, index_col="año")
    conn.close()

    return dfs

if __name__ == "__main__":
    data_dict = load_validated_tables()
    # Ejemplo: listar tablas cargadas
    print("Tablas cargadas:", list(data_dict.keys()))
