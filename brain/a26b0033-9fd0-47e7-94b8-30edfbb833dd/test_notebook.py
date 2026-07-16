import json
import sqlite3
import pandas as pd
import numpy as np
import os
import sys

# Add src and current directory to sys.path to resolve package imports
sys.path.append('.')
sys.path.append('src')

notebook_path = "notebooks/tesis/serie_completa/IDH/idh copy.ipynb"

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code":
        print(f"Executing cell {i}...")
        code = "".join(cell["source"])
        exec(code, globals())
print("Notebook executed successfully!")
