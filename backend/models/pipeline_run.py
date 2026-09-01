
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from backend.database import Base


class PipelineRun(Base):

    __tablename__ = "pipeline_runs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    pipeline_id = Column(
        Integer,
        ForeignKey("pipelines.id"),
        nullable=False
    )

    status = Column(
        String(30),
        default="RUNNING",
        nullable=False
    )

    records_processed = Column(
        Integer,
        default=0
    )

    attempt = Column(
        Integer,
        default=1,
        nullable=False
    )

    error_message = Column(
        String(1000),
        nullable=True
    )

    started_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )
