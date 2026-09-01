import pandas as pd


def clean_customer_data(df):

    df = df.copy()

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Clean string columns
    string_columns = [
        "name",
        "email",
        "city"
    ]

    for column in string_columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

    # Convert age to numeric
    if "age" in df.columns:

        df["age"] = pd.to_numeric(
            df["age"],
            errors="coerce"
        )

    # Convert customer_id to numeric
    if "customer_id" in df.columns:

        df["customer_id"] = pd.to_numeric(
            df["customer_id"],
            errors="coerce"
        )

    # Standardize email
    if "email" in df.columns:

        df["email"] = (
            df["email"]
            .str.lower()
        )

    return df 