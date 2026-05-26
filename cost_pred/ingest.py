import polars as pl

from cost_pred import PROJECT_ROOT


def ingest_dental() -> bool:

    files = [
          "data/lakehouse/raw_source/2025-05-02_Liberty_KFHP-MAS-DC-FFS_in-network-rates.json"
        , "data/lakehouse/raw_source/2025-05-02_Liberty_KFHP-MAS-MD-FFS_in-network-rates.json"
        , "data/lakehouse/raw_source/2025-05-14_Liberty_KFHP-MAS-VA-FFS_in-network-rates.json"]

    for f in files:
        df = pl.read_json(str(PROJECT_ROOT / f))
        df = df.with_columns(pl.lit(f).alias("source_file"))
        df = df.explode("in_network").unnest("in_network")
        df = df.explode("negotiated_rates").unnest("negotiated_rates")
        df = df.explode("negotiated_prices").unnest("negotiated_prices")

        df = df.select(
              pl.col("reporting_entity_name")
            , pl.col("plan_name")
            , pl.col("plan_id")
            , pl.col("plan_market_type")
            , pl.col("last_updated_on")
            , pl.col("negotiation_arrangement")
            , pl.col("name")
            , pl.col("billing_code_type")
            , pl.col("billing_code_type_version")
            , pl.col("billing_code")
            , pl.col("description")
            , pl.col("negotiated_rate")
            , pl.col("billing_class"))

        output_path = str(PROJECT_ROOT / f.replace("raw_source", "bronze").replace(".json", ".parquet"))
        df.write_parquet(output_path, compression="snappy")

    return True

if __name__ == "__main__":
    ingest_dental()