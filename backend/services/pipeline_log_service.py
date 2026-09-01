from datetime import datetime

from backend.database import SessionLocal
from backend.models.pipeline_run import PipelineRun


def create_pipeline_run(
    pipeline_id: int
):

    db = SessionLocal()

    try:

        run = PipelineRun(
            pipeline_id=pipeline_id,
            status="RUNNING",
            records_processed=0
        )

        db.add(run)

        db.commit()

        db.refresh(run)

        return run.id

    finally:

        db.close()


def complete_pipeline_run(
    run_id: int,
    status: str,
    records_processed: int = 0,
    error_message: str = None
):

    db = SessionLocal()

    try:

        run = db.query(
            PipelineRun
        ).filter(
            PipelineRun.id == run_id
        ).first()

        if run:

            run.status = status

            run.records_processed = (
                records_processed
            )

            run.error_message = (
                error_message
            )

            run.completed_at = (
                datetime.utcnow()
            )

            db.commit()

    finally:

        db.close()