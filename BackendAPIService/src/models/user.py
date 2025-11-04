from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint

from src.core.db import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("username", name="uq_user_username"), UniqueConstraint("email", name="uq_user_email"))

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), nullable=False, index=True)
    email = Column(String(256), nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    roles = Column(String(128), default="user", nullable=False)  # comma-separated roles
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
