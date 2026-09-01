from pydantic import BaseModel


class PipelineCreate(BaseModel):

    name: str

    source_type: str

    source_path: str
    