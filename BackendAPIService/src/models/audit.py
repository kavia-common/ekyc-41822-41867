from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from src.core.db import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor = Column(String(128), nullable=False)  # username or system
    action = Column(String(128), nullable=False)
    resource = Column(String(128), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
