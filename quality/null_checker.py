def check_nulls(df):

    result = {}

    for column in df.columns:

        null_count = df[column].isnull().sum()

        result[column] = {
            "null_count": int(null_count),
            "status": "PASS" if null_count == 0 else "WARNING"
        }

    return result