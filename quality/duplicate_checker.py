def check_duplicates(df):

    duplicate_rows = df.duplicated().sum()

    return {
        "duplicate_rows": int(duplicate_rows),
        "status": "PASS" if duplicate_rows == 0 else "FAIL"
    }