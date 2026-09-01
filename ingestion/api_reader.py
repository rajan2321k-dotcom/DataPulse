import requests
import pandas as pd


def read_rest_api(url: str):

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict):

            if "data" in data:
                data = data["data"]

            elif "results" in data:
                data = data["results"]

            else:
                data = [data]

        df = pd.DataFrame(data)

        return {
            "success": True,
            "source_type": "REST_API",
            "data": df,
            "records": len(df),
            "columns": list(df.columns)
        }

    except Exception as e:

        return {
            "success": False,
            "source_type": "REST_API",
            "data": None,
            "records": 0,
            "columns": [],
            "error": str(e)
        }