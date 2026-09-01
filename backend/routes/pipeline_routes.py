from fastapi import APIRouter, HTTPException

from backend.database import SessionLocal
from backend.models import Pipeline, PipelineRun
from backend.schemas.pipeline import PipelineCreate
from backend.services.pipeline_runner import run_pipeline


router = APIRouter()


# --------------------------------------------------
# CREATE PIPELINE
# --------------------------------------------------

@router.post("")
def create_pipeline(pipeline_data: PipelineCreate):

    db = SessionLocal()

    try:

        pipeline = Pipeline(
            name=pipeline_data.name,
            source_type=pipeline_data.source_type,
            source_path=pipeline_data.source_path,
            status="CREATED"
        )

        db.add(pipeline)
        db.commit()
        db.refresh(pipeline)

        return {
            "success": True,
            "message": "Pipeline created successfully",
            "pipeline": {
                "id": pipeline.id,
                "name": pipeline.name,
                "source_type": pipeline.source_type,
                "source_path": pipeline.source_path,
                "status": pipeline.status
            }
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()


# --------------------------------------------------
# GET ALL PIPELINES
# --------------------------------------------------

@router.get("")
def get_pipelines():

    db = SessionLocal()

    try:

        pipelines = (
            db.query(Pipeline)
            .order_by(Pipeline.id.asc())
            .all()
        )

        return {
            "count": len(pipelines),
            "pipelines": [
                {
                    "id": pipeline.id,
                    "name": pipeline.name,
                    "source_type": pipeline.source_type,
                    "source_path": pipeline.source_path,
                    "status": pipeline.status
                }
                for pipeline in pipelines
            ]
        }

    finally:
        db.close()


# --------------------------------------------------
# GET SINGLE PIPELINE
# --------------------------------------------------

@router.get("/{pipeline_id}")
def get_pipeline(pipeline_id: int):

    db = SessionLocal()

    try:

        pipeline = (
            db.query(Pipeline)
            .filter(Pipeline.id == pipeline_id)
            .first()
        )

        if not pipeline:

            raise HTTPException(
                status_code=404,
                detail="Pipeline not found"
            )

        return {
            "id": pipeline.id,
            "name": pipeline.name,
            "source_type": pipeline.source_type,
            "source_path": pipeline.source_path,
            "status": pipeline.status
        }

    finally:
        db.close()


# --------------------------------------------------
# RUN PIPELINE
# --------------------------------------------------

@router.post("/{pipeline_id}/run")
def execute_pipeline(pipeline_id: int):

    db = SessionLocal()

    try:

        pipeline = (
            db.query(Pipeline)
            .filter(Pipeline.id == pipeline_id)
            .first()
        )

        if not pipeline:

            raise HTTPException(
                status_code=404,
                detail="Pipeline not found"
            )

        # Create pipeline run
        pipeline_run = PipelineRun(
            pipeline_id=pipeline.id,
            status="RUNNING",
            records_processed=0,
            attempt=1
        )

        db.add(pipeline_run)
        db.commit()
        db.refresh(pipeline_run)

        # Execute pipeline
        result = run_pipeline(
            pipeline.source_type,
            pipeline.source_path
        )

        # Update run status
        if result.get("success"):

            pipeline_run.status = "SUCCESS"

            pipeline_run.records_processed = result.get(
                "records_cleaned",
                0
            )

            pipeline.status = "SUCCESS"

        else:

            pipeline_run.status = "FAILED"

            pipeline_run.records_processed = 0

            pipeline_run.error_message = result.get(
                "error",
                "Pipeline execution failed"
            )

            pipeline.status = "FAILED"

        db.commit()

        return {
            "success": result.get("success", False),
            "pipeline_id": pipeline.id,
            "pipeline_name": pipeline.name,
            "run_id": pipeline_run.id,
            "attempt": pipeline_run.attempt,
            "status": pipeline_run.status,
            "result": result
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()


# --------------------------------------------------
# GET PIPELINE RUNS
# --------------------------------------------------

@router.get("/{pipeline_id}/runs")
def get_pipeline_runs(pipeline_id: int):

    db = SessionLocal()

    try:

        pipeline = (
            db.query(Pipeline)
            .filter(Pipeline.id == pipeline_id)
            .first()
        )

        if not pipeline:

            raise HTTPException(
                status_code=404,
                detail="Pipeline not found"
            )

        runs = (
            db.query(PipelineRun)
            .filter(PipelineRun.pipeline_id == pipeline_id)
            .order_by(PipelineRun.id.desc())
            .all()
        )

        return {
            "pipeline_id": pipeline.id,
            "pipeline_name": pipeline.name,
            "count": len(runs),
            "runs": [
                {
                    "run_id": run.id,
                    "status": run.status,
                    "attempt": run.attempt,
                    "records_processed": run.records_processed,
                    "error": run.error_message,
                    "started_at": (
                        run.started_at.isoformat()
                        if run.started_at
                        else None
                    ),
                    "completed_at": (
                        run.completed_at.isoformat()
                        if run.completed_at
                        else None
                    )
                }
                for run in runs
            ]
        }

    finally:
        db.close()


@router.delete("/{pipeline_id}")
def delete_pipeline(pipeline_id: int):

    db = SessionLocal()

    try:
        pipeline = (
            db.query(Pipeline)
            .filter(Pipeline.id == pipeline_id)
            .first()
        )

        if not pipeline:
            raise HTTPException(
                status_code=404,
                detail="Pipeline not found"
            )

        # Delete pipeline runs first
        db.query(PipelineRun).filter(
            PipelineRun.pipeline_id == pipeline_id
        ).delete(
            synchronize_session=False
        )

        # Delete pipeline
        db.delete(pipeline)
        db.commit()

        return {
            "success": True,
            "message": "Pipeline deleted successfully",
            "pipeline_id": pipeline_id
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()