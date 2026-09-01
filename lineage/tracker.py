from backend.database import SessionLocal
from backend.models.lineage import Lineage


def track_lineage(
    source,
    source_type,
    target,
    operation,
    records_processed,
    status="SUCCESS"
):

    db = SessionLocal()

    try:

        record = Lineage(

            source=source,

            source_type=source_type,

            target=target,

            operation=operation,

            records_processed=records_processed,

            status=status
        )

        db.add(record)

        db.commit()

        db.refresh(record)

        return record.id

    finally:

        db.close()