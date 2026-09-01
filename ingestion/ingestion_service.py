from ingestion.csv_reader import read_csv_file
from ingestion.excel_reader import read_excel_file
from ingestion.api_reader import read_rest_api


def ingest_data(
    source_type: str,
    source: str
):

    source_type = source_type.upper()

    if source_type == "CSV":

        return read_csv_file(source)

    elif source_type == "EXCEL":

        return read_excel_file(source)

    elif source_type == "REST_API":

        return read_rest_api(source)

    else:

        return {
            "success": False,
            "error": f"Unsupported source type: {source_type}"
        }