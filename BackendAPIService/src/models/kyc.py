from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.core.db import Base


class KYCStatus:
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


class KYCCase(Base):
    __tablename__ = "kyc_cases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    full_name = Column(String(256), nullable=False)
    document_type = Column(String(64), nullable=False)  # e.g., "passport", "id_card"
    document_number = Column(String(128), nullable=False)
    document_file_path = Column(String(512), nullable=True)  # stored locally
    selfie_file_path = Column(String(512), nullable=True)  # stored locally
    status = Column(String(32), nullable=False, default=KYCStatus.PENDING)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # relationships
    user = relationship("User")
