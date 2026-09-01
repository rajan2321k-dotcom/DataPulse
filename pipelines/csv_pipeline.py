import pandas as pd


def load_csv(file_path: str):

    try:

        df = pd.read_csv(file_path)

        return {
            "success": True,
            "data": df,
            "records": len(df)
        }

    except Exception as e:

        return {
            "success": False,
            "data": None,
            "records": 0,
            "error": str(e)
        }