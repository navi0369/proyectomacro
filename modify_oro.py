import json

with open("notebooks/tesis/serie_completa/minerales/oro.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

# CELL 0
source_0 = "".join(nb['cells'][0]['source'])
source_0 = source_0.replace(
    "CYCLES=adjust_cycles(df,CYCLES)",
    "CYCLES=adjust_cycles(df,CYCLES_PERIODOS)"
)
old_offsets = """cycle_text_offsets = {
    "Expansión 87-00": (1995,0.92),
    "Transicion 01-05":    (2001,0.92),
    "Expansión 06-14": (2007.2,0.92)
}"""
new_offsets = """cycle_text_offsets = {
    "Neoliberalismo": (1995,0.92),
    "ESCP I": (2010,0.92),
    "ESCP II": (2019,0.92)
}"""
if old_offsets in source_0:
    source_0 = source_0.replace(old_offsets, new_offsets)
else:
    print("WARNING: old_offsets not found in cell 0")

nb['cells'][0]['source'] = [line + '\n' for line in source_0.split('\n')]
# clean up the last newline if it wasn't there, but json loading usually gives lists. Actually just replace and split lines correctly
nb['cells'][0]['source'] = [s + '\n' for s in source_0.splitlines()]
if not source_0.endswith('\n'):
    nb['cells'][0]['source'][-1] = nb['cells'][0]['source'][-1].rstrip('\n')

# CELL 1
source_1 = "".join(nb['cells'][1]['source'])
source_1 = source_1.replace(
    "CYCLES=adjust_cycles(df,CYCLES)",
    "CYCLES=adjust_cycles(df,CYCLES_PERIODOS)"
)
old_offsets_vol = """cycle_text_offsets_vol = {
    "Expansión 87-00": (1995,0.97),
    "Transicion 01-05":    (2001,0.97),
    "Expansión 06-14": (2008,0.97),
}"""
new_offsets_vol = """cycle_text_offsets_vol = {
    "Neoliberalismo": (1995,0.97),
    "ESCP I": (2010,0.97),
    "ESCP II": (2019,0.97),
}"""
if old_offsets_vol in source_1:
    source_1 = source_1.replace(old_offsets_vol, new_offsets_vol)
else:
    print("WARNING: old_offsets_vol not found in cell 1")

nb['cells'][1]['source'] = [s + '\n' for s in source_1.splitlines()]
if not source_1.endswith('\n'):
    nb['cells'][1]['source'][-1] = nb['cells'][1]['source'][-1].rstrip('\n')

with open("notebooks/tesis/serie_completa/minerales/oro.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
