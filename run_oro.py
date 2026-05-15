import json

with open("notebooks/tesis/serie_completa/minerales/oro.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

script = ""
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        script += "".join(cell['source']) + "\n"

with open("run_oro_test.py", "w", encoding="utf-8") as f:
    f.write(script)
