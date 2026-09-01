import pandas as pd


def validate_schema(df, expected_schema):

    results = {}
    errors = []

    # Check required columns
    for column, expected_type in expected_schema.items():

        if column not in df.columns:

            errors.append(
                f"Missing column: {column}"
            )

            results[column] = {
                "status": "FAIL",
                "reason": "Column missing"
            }

            continue

        results[column] = {
            "status": "PASS",
            "expected_type": expected_type,
            "actual_type": str(df[column].dtype)
        }

    # Check unexpected columns
    unexpected_columns = [
        column
        for column in df.columns
        if column not in expected_schema
    ]

    for column in unexpected_columns:

        results[column] = {
            "status": "WARNING",
            "reason": "Unexpected column"
        }

    return {
        "status": "PASS" if not errors else "FAIL",
        "columns": results,
        "errors": errors,
        "unexpected_columns": unexpected_columns
    }