import json
import pandas as pd

from ingestion.ingestion_service import ingest_data
from transformation.cleaner import clean_customer_data
from backend.services.database_service import save_dataframe
from lineage.tracker import track_lineage


def serialize_nested_values(records):
    cleaned_records = []

    for record in records:
        new_record = {}

        for key, value in record.items():

            if isinstance(value, (dict, list)):
                new_record[key] = json.dumps(value)

            else:
                new_record[key] = value
    
        cleaned_records.append(new_record)

    return cleaned_records


def run_pipeline(source_type, source_path):

    # 1. Extract
    ingestion_result = ingest_data(
        source_type,
        source_path
    )

    if not ingestion_result["success"]:
        return {
            "success": False,
            "stage": "INGESTION",
            "error": ingestion_result["error"]
        }

    df = ingestion_result["data"]

    records = len(df)

    # ------------------------------------------------
    # 2. Convert nested JSON values to strings
    # ------------------------------------------------

    records_list = df.to_dict(orient="records")

    records_list = serialize_nested_values(records_list)

    df = __import__("pandas").DataFrame(records_list)

    # ------------------------------------------------
    # 3. Save raw data
    # ------------------------------------------------

    raw_result = save_dataframe(
        df,
        "pipeline_raw_data"
    )

    if not raw_result["success"]:
        return {
            "success": False,
            "stage": "RAW_STORAGE",
            "error": raw_result["error"]
        }

    # ------------------------------------------------
    # 4. Clean data
    # ------------------------------------------------

    cleaned_df = clean_customer_data(df)

    # ------------------------------------------------
    # 5. Save cleaned data
    # ------------------------------------------------

    clean_result = save_dataframe(
        cleaned_df,
        "pipeline_clean_data"
    )

    if not clean_result["success"]:
        return {
            "success": False,
            "stage": "CLEAN_STORAGE",
            "error": clean_result["error"]
        }

    # ------------------------------------------------
    # 6. Track ingestion lineage
    # ------------------------------------------------

    track_lineage(
        source=source_path,
        source_type=source_type,
        target="pipeline_raw_data",
        operation="INGESTION",
        records_processed=records
    )

    # ------------------------------------------------
    # 7. Track cleaning lineage
    # ------------------------------------------------

    track_lineage(
        source="pipeline_raw_data",
        source_type="DATABASE",
        target="pipeline_clean_data",
        operation="CLEANING",
        records_processed=len(cleaned_df)
    )

    # ------------------------------------------------
    # 8. Success
    # ------------------------------------------------

    return {
        "success": True,
        "records_received": records,
        "records_cleaned": len(cleaned_df),
        "raw_table": "pipeline_raw_data",
        "clean_table": "pipeline_clean_data"
    }