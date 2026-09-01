from lineage.tracker import track_lineage


track_lineage(

    source="data/customers.csv",

    source_type="CSV",

    target="raw_customers",

    operation="CSV_INGESTION",

    records_processed=8
)


track_lineage(

    source="raw_customers",

    source_type="DATABASE",

    target="customers",

    operation="DATA_CLEANING",

    records_processed=7
)


print("Lineage tracking completed.")