import duckdb
import pytest

from cost_pred.db import get_connection, create_base_tables


def test_get_connection_returns_duckdb_connection():
    con = get_connection(":memory:")
    assert isinstance(con, duckdb.DuckDBPyConnection)
    con.close()


def test_get_connection_read_only(tmp_path):
    db_path = str(tmp_path / "test.duckdb")
    con = get_connection(db_path)
    con.execute("CREATE TABLE t (x INT)")
    con.close()

    ro_con = get_connection(db_path, read_only=True)
    with pytest.raises(duckdb.InvalidInputException):
        ro_con.execute("CREATE TABLE t2 (y INT)")
    ro_con.close()


def test_create_base_tables_creates_both_tables():
    con = get_connection(":memory:")
    create_base_tables(con)
    tables = [r[0] for r in con.sql("SHOW TABLES").fetchall()]
    assert "lib_dental_cdt" in tables
    assert "lib_dental_cost" in tables

    schema = {r[0] for r in con.sql("DESCRIBE lib_dental_cost").fetchall()}
    assert "billing_code" in schema
    assert "avg_negotiated_rate" in schema
    assert "contains_crown" in schema

    row_count = con.sql("SELECT COUNT(*) FROM lib_dental_cost").fetchone()[0]
    assert row_count > 0
    con.close()


from unittest.mock import patch
from pathlib import Path

from cost_pred.db import load_classification_results


def test_load_classification_results_missing_file_raises():
    con = get_connection(":memory:")
    with patch("cost_pred.db.SILVER_DIR", Path("nonexistent/path")):
        with pytest.raises(FileNotFoundError, match="Classification cache not found"):
            load_classification_results(con)
    con.close()
