"""Validate all tables in the project database and generate a report."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import pandas as pd
from fpdf import FPDF

from . import validators
from .validators import validate_df
from func_auxiliares.config import DB_PATH


def list_tables(conn: sqlite3.Connection) -> List[str]:
    """Return the list of tables in the SQLite database."""
    query = (
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%'"
    )
    cursor = conn.execute(query)
    return [row[0] for row in cursor.fetchall()]


def _capture_warnings() -> Tuple[List[str], Callable[[str], None]]:
    """Temporarily capture warnings emitted by :func:`validate_df`."""
    captured: List[str] = []

    def collector(msg: str) -> None:
        captured.append(msg)

    return captured, collector


def validate_table(conn: sqlite3.Connection, table: str) -> Dict[str, object]:
    """Validate a single table and return the result dictionary."""
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)

    warnings, collector = _capture_warnings()
    original = validators._warn
    try:
        # monkey patch the warning function
        validators._warn = collector  # type: ignore
        validate_df(df, table)
        status = "OK"
        error = ""
    except Exception as exc:  # noqa: BLE001
        status = "ERROR"
        error = str(exc)
    finally:
        validators._warn = original  # type: ignore

    return {
        "table": table,
        "status": status,
        "error": error,
        "warnings": warnings,
    }


def validate_database(db_path: str = DB_PATH) -> pd.DataFrame:
    """Validate every table in *db_path* and return a DataFrame of results."""
    conn = sqlite3.connect(db_path, uri=True)
    try:
        tables = list_tables(conn)
        results = [validate_table(conn, table) for table in tables]
    finally:
        conn.close()

    return pd.DataFrame(results)


def generate_report(results: pd.DataFrame, report_path: Path) -> None:
    """Create a PDF report summarizing ``results`` at ``report_path``."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Informe de Validación", ln=True, align="C")

    for _, row in results.iterrows():
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, row["table"], ln=True)

        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Estado: {row['status']}", ln=True)
        if row["error"]:
            pdf.multi_cell(0, 10, f"Error: {row['error']}")
        if row["warnings"]:
            pdf.cell(0, 10, "Advertencias:", ln=True)
            for warn in row["warnings"]:
                pdf.multi_cell(0, 10, f"- {warn}")

    pdf.output(str(report_path))


if __name__ == "__main__":
    df_results = validate_database()
    generate_report(df_results, Path("validation_report.pdf"))
    print(df_results)