"""
SQLAlchemy Base Model
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()


def generate_uuid() -> str:
    return str(uuid.uuid4())


class TimestampMixin:
    """타임스탬프 믹스인"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
