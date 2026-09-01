def check_required_columns(
    df,
    required_columns
):

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    return {
        "required_columns": required_columns,
        "missing_columns": missing_columns,
        "status": "PASS"
        if not missing_columns
        else "FAIL"
    }