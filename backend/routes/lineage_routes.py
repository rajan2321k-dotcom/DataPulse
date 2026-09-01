from fastapi import APIRouter
from sqlalchemy import text

from backend.database import engine


router = APIRouter(
    prefix="/lineage",
    tags=["Data Lineage"]
)


@router.get("")
def get_lineage():

    query = text("""
        SELECT
            id,
            source,
            source_type,
            target,
            operation,
            records_processed,
            status,
            created_at
        FROM lineage
        ORDER BY id
    """)

    with engine.connect() as connection:

        result = connection.execute(query)

        rows = result.mappings().all()

    return {
        "count": len(rows),
        "lineage": [
            dict(row)
            for row in rows
        ]
    }