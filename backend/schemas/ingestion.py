from pydantic import BaseModel


class IngestionRequest(BaseModel):
    source_type: str
    source: str