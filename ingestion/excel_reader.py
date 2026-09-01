import pandas as pd


def read_excel_file(file_path: str):

    try:
        df = pd.read_excel(file_path)

        return {
            "success": True,
            "source_type": "EXCEL",
            "data": df,
            "records": len(df),
            "columns": list(df.columns)
        }

    except Exception as e:

        return {
            "success": False,
            "source_type": "EXCEL",
            "data": None,
            "records": 0,
            "columns": [],
            "error": str(e)
        }