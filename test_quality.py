import pandas as pd

from quality.validator import validate_dataset


df = pd.read_csv(
    "data/customers.csv"
)


result = validate_dataset(
    df,
    required_columns=[
        "customer_id",
        "name",
        "email",
        "age",
        "city"
    ]
)


print("\n==============================")
print("       DATAPULSE QUALITY")
print("==============================")

print(
    "\nTotal Records:",
    result["total_records"]
)

print(
    "\nDuplicate Check:",
    result["duplicate_check"]
)

print(
    "\nNULL Check:"
)

for column, value in result["null_check"].items():

    print(
        f"{column}: {value}"
    )


print(
    "\nData Types:"
)

for column, dtype in result["datatype_check"].items():

    print(
        f"{column}: {dtype}"
    )


print(
    "\nEmail Check:",
    result["email_check"]
)

print(
    "\nRequired Columns:",
    result["required_column_check"]
)

print(
    "\n=============================="
)

print(
    "DATA QUALITY SCORE:",
    result["quality_score"],
    "%"
)

print(
    "=============================="
)