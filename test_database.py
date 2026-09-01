import pandas as pd

from backend.services.database_service import (
    save_dataframe,
    get_tables,
    read_table
)

from transformation.cleaner import (
    clean_customer_data
)


# --------------------------------
# 1. Read raw data
# --------------------------------

df = pd.read_csv(
    "data/customers.csv"
)


print("\nRAW DATA")
print("====================")

print(df)


# --------------------------------
# 2. Save raw data
# --------------------------------

raw_result = save_dataframe(
    df,
    "raw_customers"
)

print("\nRAW DATA RESULT")

print(raw_result)


# --------------------------------
# 3. Clean data
# --------------------------------

cleaned_df = clean_customer_data(
    df
)


print("\nCLEANED DATA")
print("====================")

print(cleaned_df)


# --------------------------------
# 4. Save cleaned data
# --------------------------------

clean_result = save_dataframe(
    cleaned_df,
    "customers"
)

print("\nCLEAN DATA RESULT")

print(clean_result)


# --------------------------------
# 5. Show tables
# --------------------------------

print("\nDATABASE TABLES")
print("====================")

print(
    get_tables()
)