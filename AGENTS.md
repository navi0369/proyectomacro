# Estructura del Proyecto

El proyecto está organizado en una estructura modular que facilita el análisis, visualización y documentación de datos económicos de Bolivia. Los principales componentes y carpetas son:

- **config.py, functions.py, graficas.py, llm_utils.py, dashboard_gpt.py**: Scripts principales con funciones de configuración, utilidades, generación de gráficas y dashboards.
- **assets/**: Carpeta de recursos gráficos, imágenes y salidas generadas por los análisis.
- **db/**: Contiene la base de datos principal (`proyectomacro.db`), archivos SQL, y tablas en formato Excel utilizadas para la carga y respaldo de datos.
- **notebooks/**: Notebooks Jupyter organizados por temas (análisis, pruebas, tesis, visualización) para exploración y desarrollo interactivo.
- **reports/**: Reportes, documentos, y archivos de resultados, incluyendo datos procesados y archivos de referencia.
- **scripts/**: Scripts de análisis, visualización y procesamiento de datos, organizados por subcarpetas temáticas. Importante aclarar que mediante jupytext los archivos de notebooks/** estan sincronizados con los archivos de scripts/**
- **cronograma/**: Archivos de planificación, cronogramas y estructura de gráficas.
- **readme_db.md, readme.md, readme_jupytext.md**: Documentación detallada sobre las tablas de la base de datos, el uso general del proyecto y la integración con Jupytext.

Esta estructura permite separar claramente los datos, el código, los recursos visuales y la documentación, facilitando la colaboración y el mantenimiento del proyecto.

## Convención de Código para `proyectomacro`

- **Estilo general:** Seguir la guía PEP 8 de Python.
- **Nombres de variables y funciones:** minúsculas_con_guiones_bajos (snake_case).
- **Nombres de clases:** CapitalizarCadaPalabra (CamelCase).
- **Constantes:** MAYÚSCULAS_CON_GUIONES_BAJOS.
- **Archivos y módulos:** minúsculas_con_guiones_bajos.
- **Importaciones:** Una por línea, agrupadas estándar, externas y locales.
- **Espacios:** Usar 4 espacios por nivel de indentación, sin tabulaciones.
- **Longitud de línea:** Máximo 79 caracteres por línea.
- **Documentación:** Docstrings en triple comilla para módulos, clases y funciones.
- **Comentarios:** Claros, concisos y actualizados.
- **Funciones y scripts:** Cada función debe tener una única responsabilidad clara.
- **Variables temporales o de iteración:** Usar nombres descriptivos, evitar abreviaturas ambiguas.

### Ejemplo breve

```python
# correcto
def calcular_promedio(valores):
    """Calcula el promedio de una lista de valores numéricos."""
    return sum(valores) / len(valores)

# incorrecto
def CalcularPromedio(ListaValores):
    return sum(ListaValores)/len(ListaValores)
```