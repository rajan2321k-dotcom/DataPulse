import pandas as pd

from backend.services.data_quality_service import (
    process_customer_dataset
)


df = pd.read_csv(
    "data/customers.csv"
)


result = process_customer_dataset(df)


print("\n==============================")
print("       DATAPULSE")
print("==============================")


print("\nSCHEMA STATUS:")

print(
    result["schema"]["status"]
)


print("\nBEFORE CLEANING:")

print(
    result["before_cleaning"]
)


print("\nAFTER CLEANING:")

print(
    result["after_cleaning"]
)


print("\nCLEANED DATA:")

print(
    result["cleaned_data"]
)


print("\n==============================")