# setup.py
from setuptools import setup, find_packages
import os

def read_requirements():
    """Lee requirements.txt si existe"""
    req_file = "requirements.txt"
    if os.path.exists(req_file):
        with open(req_file, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="proyecto_macro",
    version="0.1.0",
    author="Juan",
    description="Dashboard macroeconómico de Bolivia - Análisis de ciclos económicos",
    long_description="Sistema integral para análisis macroeconómico de Bolivia con visualizaciones interactivas",
    python_requires=">=3.8",
    
    # Instalar dependencies completas
    install_requires=[
        "dash>=2.14.0",
        "dash-bootstrap-components>=1.5.0", 
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "plotly>=5.15.0",
        "matplotlib>=3.7.0",
        "PyYAML>=6.0",
        "gunicorn>=21.0.0",
        "jupyter>=1.0.0",
        "jupytext>=1.15.0",
    ],
    
    # Configuración correcta de packages
    packages=[
        "func_auxiliares",
        "validation",
        "proyectomacro", 
        "proyectomacro.config",
        "proyectomacro.pages", 
        "proyectomacro.pages.cuentas_nacionales",
        "proyectomacro.pages.deuda",
        "proyectomacro.pages.empleo", 
        "proyectomacro.pages.exportaciones",
        "proyectomacro.pages.importaciones",
        "proyectomacro.pages.pobreza",
        "proyectomacro.pages.precios_y_produccion",
        "proyectomacro.pages.sector_externo",
        "proyectomacro.pages.sector_fiscal", 
        "proyectomacro.pages.sector_monetario",
        "proyectomacro.validation",
    ],
    
    # Mapeo correcto de directorios
    package_dir={
        "proyectomacro": "src/proyectomacro",
        "func_auxiliares": "func_auxiliares",
        "validation": "src/proyectomacro/validation",
    },
    
    # Incluir archivos de datos y configuración
    package_data={
        "proyectomacro": [
            "assets/*",
            "config/*.yml",
            "config/*.yaml",
        ],
        "func_auxiliares": ["*.py"],
        "": ["*.yml", "*.yaml", "*.csv", "*.db"],
    },
    
    # Archivos adicionales a incluir
    include_package_data=True,
    
    # Entry points para ejecutar el dashboard
    entry_points={
        "console_scripts": [
            "proyecto-macro=proyectomacro.app:main",
        ],
    },
    
    # Clasificadores
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
