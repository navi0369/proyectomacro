import json

notebooks = [
    "notebooks/tesis/serie_completa/oferta_total/oferta_total.ipynb",
    "notebooks/tesis/serie_completa/operaciones_empresas_publicas/operaciones_empresas_publicas.ipynb",
    "notebooks/tesis/serie_completa/ingresos_corrientes/ingresos_corrientes.ipynb",
    "notebooks/tesis/serie_completa/ingresos_tributarios/ingresos_tributarios.ipynb"
]

for nb_path in notebooks:
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
    src = "".join(nb["cells"][0]["source"])
    print(f"--- {nb_path} ---")
    start = src.find("5. OFFSETS DE POSICIONAMIENTO")
    end = src.find("6. PLOTEO")
    if start != -1 and end != -1:
        print(src[start:end])
