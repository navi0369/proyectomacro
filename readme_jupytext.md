# 1. Instalación de Jupytext
pip install jupytext

# 2. Habilitar globstar en Bash
shopt -s globstar

# 3. Configuración global (un solo vez)
#    Crea jupytext.toml en la raíz con:
#    formats = "notebooks///ipynb,scripts///py:percent"

# 4. Emparejar subcarpetas existentes (solo primera vez)
jupytext --set-formats "notebooks/analysis///ipynb,scripts/analysis///py:percent" "notebooks/analysis/**/*.ipynb"
jupytext --set-formats "notebooks/tesis///ipynb,scripts/tesis///py:percent"         "notebooks/tesis/**/*.ipynb"
# … repite para cada carpeta que quieras emparejar
# 4.1) Define el emparejamiento para que cada script genere su .ipynb espejo
jupytext --set-formats \
  "notebooks/tesis/serie_completa/finanzas///ipynb,scripts/tesis/serie_completa/finanzas///py:percent" \
  "scripts/tesis/serie_completa/finanzas/**/*.py"

# 4.2) Sincroniza: crea/actualiza los .ipynb a partir de los .py
jupytext --sync "scripts/tesis/serie_completa/finanzas/**/*.py"



# 5. Cada vez que edites un .ipynb → regenerar .py
jupytext --sync "notebooks/analysis/**/*.ipynb"
jupytext --sync "notebooks/tesis/**/*.ipynb"

# 6. Cada vez que edites un .py → regenerar .ipynb
jupytext --sync "scripts/analysis/**/*.py"
jupytext --sync "scripts/tesis/**/*.py"

# 7. Para ignorar notebooks corruptos sin abortar
jupytext --warn-only --sync "notebooks/**/*.ipynb"