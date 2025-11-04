from typing import Optional
from sqlalchemy.orm import Session

from src.models.audit import AuditLog


def write_audit(db: Session, actor: str, action: str, resource: str, details: Optional[str] = None) -> None:
    """Write an audit log record."""
    record = AuditLog(actor=actor, action=action, resource=resource, details=details)
    db.add(record)
    db.commit()
