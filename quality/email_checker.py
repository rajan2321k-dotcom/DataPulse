import re


EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


def check_emails(df, column="email"):

    if column not in df.columns:

        return {
            "status": "SKIPPED",
            "message": f"{column} column not found"
        }

    invalid_count = 0

    for value in df[column].dropna():

        if not re.match(EMAIL_PATTERN, str(value)):

            invalid_count += 1

    return {
        "column": column,
        "invalid_emails": invalid_count,
        "status": "PASS" if invalid_count == 0 else "FAIL"
    }