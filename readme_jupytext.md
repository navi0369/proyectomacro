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

# 5. Cada vez que edites un .ipynb → regenerar .py
jupytext --sync "notebooks/analysis/**/*.ipynb"
jupytext --sync "notebooks/tesis/serie_completa/**/*.ipynb"

# 6. Cada vez que edites un .py → regenerar .ipynb
jupytext --sync "scripts/analysis/**/*.py"
jupytext --sync "scripts/tesis/**/*.py"

# 7. Para ignorar notebooks corruptos sin abortar
jupytext --warn-only --sync "notebooks/**/*.ipynb"


turso db shell proyectomacro .dump > proyectomacro.sql
sqlite3 proyectomacro.db < proyectomacro.sql


jupytext --sync notebooks/tesis/serie_completa/exportaciones/*.ipynb

touch notebooks/tesis/serie_completa/exportaciones/*.ipynb

git log -1 ff3c2d0 \
  --pretty=format:'### %h – %s (%ad)%n' \
  --date=short \
  --patch \
  --no-color \
  -- '*.py' \
  > 2025-06-22.2.md


# Crea un archivo .ipynb vacío en cada subcarpeta de serie_completa
for dir in notebooks/tesis/serie_completa/*/; do
  touch "${dir}"*.ipynb
done
# para actualizar una sola carpeta
touch mi_carpeta/*.ipynb

# Sincroniza con jupytext todos los .ipynb de cada subcarpeta de serie_completa
for dir in notebooks/tesis/serie_completa/*/; do
  jupytext --sync "${dir}"*.ipynb
done

for dir in notebooks/tesis/*/; do
  jupytext --sync "${dir}"*.ipynb
done

export PYTHONPATH=src          # opcional, si tu árbol no está en PYTHONPATH
python -m proyectomacro.validation.validate_all