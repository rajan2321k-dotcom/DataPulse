from ingestion.ingestion_service import ingest_data


url = "https://jsonplaceholder.typicode.com/users"


result = ingest_data(
    "REST_API",
    url
)


print("Success:", result["success"])
print("Source:", result["source_type"])
print("Records:", result["records"])
print("Columns:", result["columns"])

if result["success"]:

    print("\nData:")
    print(result["data"].head())

else:

    print("Error:", result["error"])