from setuptools import setup, find_packages

setup(
    name="func_auxiliares",         # Nombre de tu paquete
    version="0.1.0",            # Versión inicial
    packages=find_packages(),   # Detecta automáticamente mi_paquete
    author="Juan",         # Opcional, para documentación
    description="Funciones utilitarias para graficas macro",  # Breve descripción
    python_requires=">=3.8",    # Rango de versiones de Python
)
