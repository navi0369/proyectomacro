# src/proyectomacro/validation/validators.py
"""
Motor genérico que aplica las reglas de TableRule a un DataFrame.

Uso:
    from validators import validate_df
    validate_df(df, "PIB_Real_Gasto")   # lanza error o emite warnings
"""

import logging
from typing import Dict

import pandas as pd
from pandas.api.types import (
    is_integer_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
)

from .rules import load_rules, TableRule

# ---------------------------------------------------------------------
# Configura logging (puedes ajustarlo en tu app principal)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
)

_rules: Dict[str, TableRule] = load_rules()


def _warn(msg: str) -> None:
    """Wrapper para warnings."""
    logging.warning(msg)


# ---------------------------------------------------------------------
def validate_df(df: pd.DataFrame, table: str) -> bool:
    """
    Valida un DataFrame según las reglas de `table`.

    Lanza:
        - ValueError, TypeError, KeyError en fallos críticos
    Devuelve:
        - True si todo está OK (solo warnings emitidos)
    """
    rule: TableRule = _rules.get(table, TableRule())

    # -----------------------------------------------------------------
    # 0. Colocar índice
    if rule.index not in df.columns and df.index.name != rule.index:
        raise KeyError(
            f"{table}: no se encuentra la columna índice '{rule.index}'"
        )

    if df.index.name != rule.index:
        df = df.set_index(rule.index)

    idx = df.index

    # -----------------------------------------------------------------
    # 1. Índice debe ser año (entero) si se solicita
    if rule.check_index_is_year:
        if not is_integer_dtype(idx):
            raise TypeError(f"{table}: índice debe ser entero (año)")

    # -----------------------------------------------------------------
    # 2. Índice único
    if rule.check_unique_index and not idx.is_unique:
        dup = idx[idx.duplicated()].unique().tolist()
        raise ValueError(f"{table}: índices duplicados {dup}")

    # -----------------------------------------------------------------
    # 3. Índice monotónico creciente
    if rule.check_monotonic_index and not idx.is_monotonic_increasing:
        _warn(f"{table}: índice no está en orden cronológico")

    # -----------------------------------------------------------------
    # 4. Columnas requeridas
    if rule.check_required_columns:
        missing = [c for c in rule.value_cols if c not in df.columns]
        if missing:
            raise KeyError(f"{table}: faltan columnas {missing}")

    # -----------------------------------------------------------------
    # 5. No Nulls
    if rule.check_no_nulls:
        nulos = df[rule.value_cols].isnull().sum()
        if nulos.any():
            _warn(f"{table}: nulos detectados {nulos[nulos>0].to_dict()}")

    # -----------------------------------------------------------------
    # 6. Tipo numérico
    if rule.check_numeric:
        non_num = [c for c in rule.value_cols if not is_numeric_dtype(df[c])]
        if non_num:
            raise TypeError(f"{table}: columnas no numéricas {non_num}")

    # -----------------------------------------------------------------
    # 7. Gaps en la secuencia
    if rule.check_gaps and len(idx) > 1:
        dif = idx.to_series().diff().dropna()
        mode_gap = dif.mode()[0] if not dif.mode().empty else None
        if mode_gap is not None and (dif != mode_gap).any():
            gaps = sorted(set(range(idx.min(), idx.max() + 1)) - set(idx))
            _warn(f"{table}: huecos en los años {gaps}")

    # -----------------------------------------------------------------
    # 8. Outliers simples (> 4 desviaciones estándar del cambio interanual)
    if rule.check_outliers:
        for col in rule.value_cols:
            delta = df[col].diff().abs().dropna()
            if delta.empty:
                continue
            thr = delta.std() * 4
            outs = delta[delta > thr]
            if not outs.empty:
                _warn(f"{table}: outliers en {col} años {outs.index.tolist()}")

    return True
