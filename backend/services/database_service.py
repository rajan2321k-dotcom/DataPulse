import pandas as pd
from sqlalchemy import create_engine, inspect

DATABASE_URL = "sqlite:///./datapulse.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


def save_dataframe(
    df: pd.DataFrame,
    table_name: str,
    if_exists: str = "replace"
):

    try:

        df.to_sql(
            table_name,
            con=engine,
            if_exists=if_exists,
            index=False
        )

        return {
            "success": True,
            "table": table_name,
            "records": len(df)
        }

    except Exception as e:

        return {
            "success": False,
            "table": table_name,
            "records": 0,
            "error": str(e)
        }


def get_tables():

    inspector = inspect(engine)

    return inspector.get_table_names()


def read_table(table_name: str):

    try:

        df = pd.read_sql_table(
            table_name,
            con=engine
        )

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