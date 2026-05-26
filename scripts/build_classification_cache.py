"""
Run the Anthropic Haiku LLM classification for all CDT codes and cache results.

Usage:
    uv run python3 scripts/build_classification_cache.py

Requires ANTHROPIC_API_KEY set in .env file.
"""
import json
from pathlib import Path

import duckdb
import polars as pl

from cost_pred.db import get_connection, create_base_tables, PROJECT_ROOT, SILVER_DIR
from cost_pred.llm import get_api_key, determine_product_fit


def build_cache() -> None:
    api_key = get_api_key()
    if api_key is None:
        raise RuntimeError("ANTHROPIC_API_KEY not found. Check your .env file.")

    con = get_connection()
    create_base_tables(con)

    codes = con.sql("""
        SELECT DISTINCT billing_code, code_desc
        FROM lib_dental_cost
        ORDER BY billing_code
    """).fetchall()

    print(f"Classifying {len(codes)} unique CDT codes...")

    results = []
    for i, (code, desc) in enumerate(codes):
        raw = determine_product_fit(code, desc, api_key)
        try:
            parsed = json.loads(raw)
            response = parsed.get("response", "PARSE_ERROR")
            reasoning = parsed.get("reasoning", raw)
        except json.JSONDecodeError:
            response = "PARSE_ERROR"
            reasoning = raw

        results.append({
            "billing_code": code,
            "code_desc": desc,
            "classification": response,
            "reasoning": reasoning,
        })

        if (i + 1) % 10 == 0:
            print(f"  ...classified {i + 1}/{len(codes)}")

    df = pl.DataFrame(results)

    silver_path = PROJECT_ROOT / SILVER_DIR
    silver_path.mkdir(parents=True, exist_ok=True)
    output_path = silver_path / "classification_results.parquet"
    df.write_parquet(output_path, compression="snappy")
    print(f"Wrote {len(results)} classifications to {output_path}")

    con.close()


if __name__ == "__main__":
    build_cache()
