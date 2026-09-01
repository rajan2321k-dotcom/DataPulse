from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from backend.database import Base


class Pipeline(Base):

    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False
    )

    source_type = Column(
        String(50),
        nullable=False
    )

    source_path = Column(
        String(255),
        nullable=True
    )

    status = Column(
        String(30),
        default="CREATED"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )