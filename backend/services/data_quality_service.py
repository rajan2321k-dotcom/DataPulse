from quality.validator import validate_dataset
from quality.schema_validator import validate_schema
from quality.schemas import CUSTOMER_SCHEMA

from transformation.cleaner import (
    clean_customer_data
)


def process_customer_dataset(df):

    # Step 1: Schema validation
    schema_result = validate_schema(
        df,
        CUSTOMER_SCHEMA
    )

    # Step 2: Quality validation
    quality_result = validate_dataset(
        df,
        required_columns=list(
            CUSTOMER_SCHEMA.keys()
        )
    )

    # Step 3: Cleaning
    cleaned_df = clean_customer_data(df)

    # Step 4: Quality after cleaning
    cleaned_quality = validate_dataset(
        cleaned_df,
        required_columns=list(
            CUSTOMER_SCHEMA.keys()
        )
    )

    return {

        "schema": schema_result,

        "before_cleaning": {
            "records": len(df),
            "quality_score":
                quality_result["quality_score"]
        },

        "after_cleaning": {
            "records": len(cleaned_df),
            "quality_score":
                cleaned_quality["quality_score"]
        },

        "cleaned_data": cleaned_df
    }