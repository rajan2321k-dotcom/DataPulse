import pandas as pd
import os
import re


def clean_csv(input_file: str, output_file: str):

    # --------------------------------------------------
    # READ CSV
    # --------------------------------------------------

    df = pd.read_csv(input_file)

    original_records = len(df)

    # --------------------------------------------------
    # CLEAN COLUMN NAMES
    # --------------------------------------------------

    df.columns = [
        str(column).strip().lower().replace(" ", "_")
        for column in df.columns
    ]

    # --------------------------------------------------
    # COUNT MISSING VALUES
    # --------------------------------------------------

    missing_values = int(
        df.isna().sum().sum()
    )

    # --------------------------------------------------
    # REMOVE COMPLETELY EMPTY ROWS
    # --------------------------------------------------

    df = df.dropna(how="all")

    # --------------------------------------------------
    # CLEAN STRING VALUES
    # --------------------------------------------------

    for column in df.columns:

        if pd.api.types.is_string_dtype(df[column]):

            df[column] = df[column].apply(
                lambda value:
                value.strip()
                if isinstance(value, str)
                else value
            )

    # --------------------------------------------------
    # DETECT NUMERIC COLUMNS
    # --------------------------------------------------

    for column in df.columns:

        # Try converting object/string columns
        # to numeric when possible

        if df[column].dtype == "object":

            converted = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            # If most values are numeric,
            # treat column as numeric

            non_empty = df[column].notna().sum()

            numeric_values = converted.notna().sum()

            if (
                non_empty > 0
                and numeric_values / non_empty >= 0.7
            ):

                df[column] = converted

    # --------------------------------------------------
    # HANDLE MISSING VALUES
    # --------------------------------------------------

    for column in df.columns:

        if pd.api.types.is_numeric_dtype(
            df[column]
        ):

            # Numeric column
            median_value = df[column].median()

            if pd.isna(median_value):
                median_value = 0

            df[column] = df[column].fillna(
                median_value
            )

        else:

            # Text column
            df[column] = df[column].fillna(
                "Unknown"
            )

    # --------------------------------------------------
    # EMAIL VALIDATION
    # --------------------------------------------------

    email_columns = [
        column
        for column in df.columns
        if "email" in column.lower()
    ]

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    invalid_values = 0

    for column in email_columns:

        for index in df.index:

            value = df.at[index, column]

            if (
                pd.isna(value)
                or str(value) == "Unknown"
            ):
                continue

            if not re.match(
                email_pattern,
                str(value)
            ):

                invalid_values += 1

                df.at[
                    index,
                    column
                ] = "Unknown"

    # --------------------------------------------------
    # AGE VALIDATION
    # --------------------------------------------------

    age_columns = [
        column
        for column in df.columns
        if column.lower() == "age"
    ]

    for column in age_columns:

        original_nulls = df[column].isna().sum()

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        new_invalid = (
            df[column].isna().sum()
            - original_nulls
        )

        invalid_values += max(
            0,
            int(new_invalid)
        )

        median_value = df[column].median()

        if pd.isna(median_value):
            median_value = 0

        df[column] = df[column].fillna(
            median_value
        )

    # --------------------------------------------------
    # PHONE CLEANING
    # --------------------------------------------------

    phone_columns = [
        column
        for column in df.columns
        if "phone" in column.lower()
    ]

    for column in phone_columns:

        df[column] = df[column].apply(
            lambda value:
            re.sub(
                r"\D",
                "",
                str(value)
            )
            if (
                not pd.isna(value)
                and str(value) != "Unknown"
            )
            else "Unknown"
        )

    # --------------------------------------------------
    # SAVE CLEANED CSV
    # --------------------------------------------------

    output_directory = os.path.dirname(
        output_file
    )

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True
        )

    df.to_csv(
        output_file,
        index=False
    )

    # --------------------------------------------------
    # RESULT
    # --------------------------------------------------

    cleaned_records = len(df)

    return {
        "success": True,

        "original_records":
            original_records,

        "cleaned_records":
            cleaned_records,

        "missing_values":
            missing_values,

        "invalid_values":
            invalid_values,

        "output_file":
            output_file
    }   