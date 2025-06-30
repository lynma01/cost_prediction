# %%
from cost_pred.ingest_lib_dental import ingest_dental
from cost_pred.lms_prompt import dental_cement

import duckdb 
from duckdb.typing import DuckDBPyType as dbpt
# %%

with duckdb.connect("cdc_cost.duckdb") as con:

    # completes the set-up, ingestion
    con.execute("""
            CREATE OR REPLACE TABLE lib_dental_cdt as 
                SELECT * FROM read_parquet("data/lakehouse/bronze/2025-05-02_Liberty*")""")

    con.execute("""
            CREATE OR REPLACE MACRO contains_text(c, t) AS
                CASE WHEN contains(UPPER(c), UPPER(t)) THEN TRUE ELSE FALSE END""")

    con.execute("""
            CREATE OR REPLACE TABLE lib_dental_cost AS 
                SELECT DISTINCT
                  reporting_entity_name
                , plan_name
                , plan_id
                , plan_market_type
                , last_updated_on
                , negotiation_arrangement
                , "name"
                , billing_code_type
                , billing_code_type_version
                , billing_class
                , billing_code
                , description as code_desc
                , contains_text(description, 'crown') as contains_crown
                , contains_text(description, 'bridge') as contains_bridge
                , contains_text(description, 'implant') as contains_implant
                , contains_text(description, 'filling') as contains_filling
                , ROUND(min(negotiated_rate), 2) as min_negotiated_rate
                , ROUND(max(negotiated_rate), 2) as max_negotiated_rate
                , ROUND((max(negotiated_rate) - min(negotiated_rate)), 2) as dif_negotiated_rate
                , ROUND(avg(negotiated_rate), 2) as avg_negotiated_rate

                FROM lib_dental_cdt

                GROUP BY all 
                ORDER BY avg_negotiated_rate DESC""")

# %%

# analysis commands
with duckdb.connect("cdc_cost.duckdb") as con:

    # adds UDF functions
    con.create_function("dental_cement", dental_cement, [dbpt(str), dbpt(str), dbpt(str)], dbpt(str))

    con.execute("""
        CREATE OR REPLACE TABLE lib_dental_deepseek AS
            SELECT DISTINCT 
                  billing_code
                , code_desc
                , dental_cement(billing_code, code_desc, 'deepseek/deepseek-r1-0528-qwen3-8b') as dc_result
                , min_negotiated_rate
                , max_negotiated_rate
                , dif_negotiated_rate

            FROM lib_dental_cost""")

    con.sql("""SELECT * FROM lib_dental_deepseek""").show()