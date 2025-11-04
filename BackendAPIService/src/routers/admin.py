from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.core.security import require_roles
from src.models.user import User
from src.models.kyc import KYCCase, KYCStatus

router = APIRouter()


@router.get("/stats", summary="System statistics", description="Basic administrative statistics.", tags=["Admin"])
def stats(_: User = Depends(require_roles(["admin"])), db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_cases = db.query(KYCCase).count()
    verified = db.query(KYCCase).filter(KYCCase.status == KYCStatus.VERIFIED).count()
    pending = db.query(KYCCase).filter(KYCCase.status == KYCStatus.PENDING).count()
    rejected = db.query(KYCCase).filter(KYCCase.status == KYCStatus.REJECTED).count()
    return {
        "users": total_users,
        "kyc_cases": total_cases,
        "kyc_verified": verified,
        "kyc_pending": pending,
        "kyc_rejected": rejected,
    }
