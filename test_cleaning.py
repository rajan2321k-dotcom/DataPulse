import pandas as pd

from transformation.cleaner import (
    clean_customer_data
)


df = pd.read_csv(
    "data/customers.csv"
)

print("\nBEFORE CLEANING")
print("====================")

print(df)

cleaned_df = clean_customer_data(df)

print("\nAFTER CLEANING")
print("====================")

print(cleaned_df)

print("\nOriginal records:",
      len(df))

print("Cleaned records:",
      len(cleaned_df))