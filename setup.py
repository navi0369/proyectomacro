# setup.py
from setuptools import setup, find_packages

setup(
    name="proyecto_macro",              # nombre del distribution package
    version="0.1.0",
    author="Juan",
    description="Dashboard macroeconómico y utilitarios",
    python_requires=">=3.8",
    install_requires=[
        "dash",
        "dash-bootstrap-components",
        "pandas",
        "plotly",
        # agregá lo que uses (e.g., sqlalchemy, pyyaml, etc.)
    ],
    packages=find_packages(
        include=[
            "func_auxiliares",
            "func_auxiliares.*",
            "proyectomacro",
            "proyectomacro.*",
        ],
        where="."
    ),
    package_dir={
        "proyectomacro": "src/proyectomacro",  # mapea el paquete fuera de la raíz
        # func_auxiliares está en la raíz, no necesita mapeo explícito
    },
    entry_points={
        "console_scripts": [
            "run-dashboard=proyectomacro.app:main",  # opcional si exportás un entrypoint
        ],
    },
)
