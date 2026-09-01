import pandas as pd


def read_csv_file(file_path: str):

    try:
        df = pd.read_csv(file_path)

        return {
            "success": True,
            "source_type": "CSV",
            "data": df,
            "records": len(df),
            "columns": list(df.columns)
        }

    except Exception as e:

        return {
            "success": False,
            "source_type": "CSV",
            "data": None,
            "records": 0,
            "columns": [],
            "error": str(e)
        }