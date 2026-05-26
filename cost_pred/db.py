import duckdb
from pathlib import Path

from cost_pred import PROJECT_ROOT

DB_PATH = "data/cdc_cost.duckdb"
BRONZE_DIR = Path("data/lakehouse/bronze")
SILVER_DIR = Path("data/lakehouse/silver")


def get_connection(path: str = DB_PATH, read_only: bool = False) -> duckdb.DuckDBPyConnection:
    resolved = str(PROJECT_ROOT / path) if not Path(path).is_absolute() and path != ":memory:" else path
    return duckdb.connect(resolved, read_only=read_only)


def create_base_tables(con: duckdb.DuckDBPyConnection) -> None:
    bronze_glob = str(PROJECT_ROOT / BRONZE_DIR / "*_in-network-rates.parquet")

    con.execute(f"""
        CREATE OR REPLACE TABLE lib_dental_cdt AS
            SELECT * FROM read_parquet('{bronze_glob}')
    """)

    con.execute("""
        CREATE OR REPLACE MACRO contains_text(c, t) AS
            CASE WHEN contains(UPPER(c), UPPER(t)) THEN TRUE ELSE FALSE END
    """)

    con.execute("""
        CREATE OR REPLACE TABLE lib_dental_cost AS
            SELECT DISTINCT
                  reporting_entity_name
                , plan_name
                , plan_id
                , plan_market_type
                , last_updated_on
                , negotiation_arrangement
                , name
                , billing_code_type
                , billing_code_type_version
                , billing_class
                , billing_code
                , description AS code_desc
                , contains_text(description, 'crown') AS contains_crown
                , contains_text(description, 'inlay') AS contains_inlay
                , contains_text(description, 'filling') AS contains_filling
                , ROUND(min(negotiated_rate), 2) AS min_negotiated_rate
                , ROUND(max(negotiated_rate), 2) AS max_negotiated_rate
                , ROUND((max(negotiated_rate) - min(negotiated_rate)), 2) AS dif_negotiated_rate
                , ROUND(avg(negotiated_rate), 2) AS avg_negotiated_rate
            FROM lib_dental_cdt
            GROUP BY ALL
            ORDER BY avg_negotiated_rate DESC
    """)


def load_classification_results(con: duckdb.DuckDBPyConnection) -> None:
    cache_path = PROJECT_ROOT / SILVER_DIR / "classification_results.parquet"
    if not cache_path.exists():
        raise FileNotFoundError(
            f"Classification cache not found at {cache_path}. "
            "Run 'uv run python3 scripts/build_classification_cache.py' first."
        )

    con.execute(f"""
        CREATE OR REPLACE TABLE lib_dental_deepseek AS
            SELECT * FROM read_parquet('{cache_path}')
    """)
