from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from backend.database import Base


class Lineage(Base):

    __tablename__ = "lineage"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    source = Column(
        String(255),
        nullable=False
    )

    source_type = Column(
        String(50),
        nullable=False
    )

    target = Column(
        String(255),
        nullable=False
    )

    operation = Column(
        String(100),
        nullable=False
    )

    records_processed = Column(
        Integer,
        default=0
    )

    status = Column(
        String(30),
        default="SUCCESS"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )