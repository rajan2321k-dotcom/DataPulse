from quality.duplicate_checker import check_duplicates
from quality.null_checker import check_nulls
from quality.datatype_checker import get_datatypes
from quality.email_checker import check_emails
from quality.required_column_checker import (
    check_required_columns
)
from quality.quality_score import (
    calculate_quality_score
)


def validate_dataset(
    df,
    required_columns=None
):

    if required_columns is None:

        required_columns = []

    total_records = len(df)

    # Duplicate check
    duplicate_result = check_duplicates(df)

    duplicate_count = duplicate_result[
        "duplicate_rows"
    ]

    # NULL check
    null_result = check_nulls(df)

    null_count = sum(
        item["null_count"]
        for item in null_result.values()
    )

    # Datatype check
    datatype_result = get_datatypes(df)

    # Email check
    email_result = check_emails(df)

    invalid_email_count = 0

    if email_result["status"] != "SKIPPED":

        invalid_email_count = email_result[
            "invalid_emails"
        ]

    # Required columns
    required_result = check_required_columns(
        df,
        required_columns
    )

    # Quality score
    quality_score = calculate_quality_score(
        total_records,
        duplicate_count,
        null_count,
        invalid_email_count
    )

    return {

        "total_records": total_records,

        "duplicate_check": duplicate_result,

        "null_check": null_result,

        "datatype_check": datatype_result,

        "email_check": email_result,

        "required_column_check": required_result,

        "quality_score": quality_score
    }