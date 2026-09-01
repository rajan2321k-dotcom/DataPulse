from fastapi import APIRouter, HTTPException

from backend.schemas.ingestion import IngestionRequest
from ingestion.ingestion_service import ingest_data


router = APIRouter(
    prefix="/ingest",
    tags=["Data Ingestion"]
)


@router.post("")
def ingest(request: IngestionRequest):

    result = ingest_data(
        request.source_type,
        request.source
    )

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result.get("error", "Ingestion failed")
        )

    return {
        "success": True,
        "source_type": result["source_type"],
        "records": result["records"],
        "columns": result["columns"]
    }