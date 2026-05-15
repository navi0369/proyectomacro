import json
import sqlite3
import pandas as pd
import re
from pathlib import Path

notebooks = [
    "notebooks/tesis/serie_completa/oferta_total/oferta_total.ipynb",
    "notebooks/tesis/serie_completa/operaciones_empresas_publicas/operaciones_empresas_publicas.ipynb",
    "notebooks/tesis/serie_completa/ingresos_corrientes/ingresos_corrientes.ipynb",
    "notebooks/tesis/serie_completa/ingresos_tributarios/ingresos_tributarios.ipynb"
]

db_path = "db/proyectomacro.db"

with sqlite3.connect(db_path) as conn:
    for nb_path in notebooks:
        with open(nb_path, "r", encoding="utf-8") as f:
            nb = json.load(f)
            
        src = "".join(nb["cells"][0]["source"])
        
        table_name = Path(nb_path).stem
        try:
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            max_vals = df.max(numeric_only=True)
        except Exception as e:
            print(f"Skipping db for {table_name}: {e}")
            max_vals = {}
            
        # Update hitos_offset_periodos to 0.8
        src = re.sub(r'hitos_offset_periodos\s*=\s*\{year:\s*[\d\.]+\s*for year in hitos_v_periodos\}', 
                     'hitos_offset_periodos = {year: 0.8 for year in hitos_v_periodos}', src)
        
        # Update medias_offsets relative heights to 0.83
        # Look for tuples like (1960, 0.90) in medias_offsets block
        # We'll just replace all (year, 0.xx) in medias_offsets with (year, 0.83)
        if "medias_offsets = {" in src:
            start_idx = src.find("medias_offsets = {")
            end_idx = src.find("}", start_idx)
            if end_idx != -1:
                block = src[start_idx:end_idx+1]
                new_block = re.sub(r'(\(\d{4},\s*)0\.\d+\)', r'\g<1>0.83)', block)
                src = src[:start_idx] + new_block + src[end_idx+1:]
                
        # Update tasas_offsets relative heights to 0.63
        if "tasas_offsets = {" in src:
            start_idx = src.find("tasas_offsets = {")
            end_idx = src.find("}", start_idx)
            if end_idx != -1:
                block = src[start_idx:end_idx+1]
                new_block = re.sub(r'(\(\d{4},\s*)0\.\d+\)', r'\g<1>0.63)', block)
                src = src[:start_idx] + new_block + src[end_idx+1:]

        # Update annotation_offsets
        if "annotation_offsets = {" in src:
            start_idx = src.find("annotation_offsets = {")
            end_idx = src.find("}", start_idx)
            # Find the closing brace of annotation_offsets. Since it's nested, we might need a better way.
            # Actually, we can just replace all (0, 0) inside annotation_offsets with the column's offset!
            # Let's iterate through columns.
            for col in max_vals.keys():
                offset = max_vals[col] * 0.05
                # find the block for this column: e.g. 'oferta_total': { ... }
                col_match = re.search(fr"'{col}'\s*:\s*\{{([^}}]+)\}}", src) or re.search(fr'"{col}"\s*:\s*\{{([^}}]+)\}}', src)
                if col_match:
                    inner_block = col_match.group(1)
                    # Replace (0, 0) or (0, 0.0) with (0, int(offset))
                    # careful not to replace something else.
                    # since we want to standardize, let's just parse the inner block and replace all (x, y) with (0, offset)
                    new_inner_block = re.sub(r'\(\s*\d+\s*,\s*[\d\.\-]+\s*\)', f'(0, {int(offset)})', inner_block)
                    src = src[:col_match.start(1)] + new_inner_block + src[col_match.end(1):]

        # Put back into notebook
        nb["cells"][0]["source"] = [line + ("\n" if not line.endswith("\n") else "") for line in src.split("\n")]
        # remove the last empty newline if split created it
        if nb["cells"][0]["source"][-1] == "\n":
            nb["cells"][0]["source"].pop()
            
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            
    print("Done updating notebooks.")
