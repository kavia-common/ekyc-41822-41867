import os
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.db import get_db
from src.core.security import get_current_user, require_roles
from src.models.kyc import KYCCase, KYCStatus
from src.models.user import User
from src.schemas.kyc import KYCOut, KYCUpdate
from src.utils.audit import write_audit

router = APIRouter()


def _save_upload(file: Optional[UploadFile], subdir: str) -> Optional[str]:
    if file is None:
        return None
    os.makedirs(os.path.join(settings.STORAGE_DIR, subdir), exist_ok=True)
    safe_name = file.filename.replace("/", "_").replace("\\", "_")
    path = os.path.join(settings.STORAGE_DIR, subdir, safe_name)
    with open(path, "wb") as f:
        f.write(file.file.read())
    return path


@router.post(
    "/cases",
    response_model=KYCOut,
    summary="Submit KYC case",
    description="Create a KYC case with optional document and selfie uploads.",
)
async def create_kyc_case(
    full_name: str = Form(...),
    document_type: str = Form(...),
    document_number: str = Form(...),
    notes: Optional[str] = Form(None),
    document_file: Optional[UploadFile] = File(None),
    selfie_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    doc_path = _save_upload(document_file, subdir=f"user_{current_user.id}")
    selfie_path = _save_upload(selfie_file, subdir=f"user_{current_user.id}")
    case = KYCCase(
        user_id=current_user.id,
        full_name=full_name,
        document_type=document_type,
        document_number=document_number,
        document_file_path=doc_path,
        selfie_file_path=selfie_path,
        status=KYCStatus.PENDING,
        notes=notes,
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    write_audit(db, actor=current_user.username, action="kyc_submit", resource="kyc_cases", details=f"case_id={case.id}")
    return case


@router.get(
    "/cases/me",
    response_model=List[KYCOut],
    summary="List my KYC cases",
    description="List KYC cases submitted by the current user.",
)
def list_my_kyc_cases(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(KYCCase).filter(KYCCase.user_id == current_user.id).order_by(KYCCase.id.desc()).all()


@router.get(
    "/cases",
    response_model=List[KYCOut],
    summary="List all KYC cases",
    description="List all KYC cases (admin only).",
)
def list_all_kyc_cases(db: Session = Depends(get_db), _: User = Depends(require_roles(["admin"]))):
    return db.query(KYCCase).order_by(KYCCase.id.desc()).all()


@router.put(
    "/cases/{case_id}",
    response_model=KYCOut,
    summary="Update KYC case status",
    description="Update KYC case status and notes (admin only).",
)
def update_kyc_case(case_id: int, body: KYCUpdate, db: Session = Depends(get_db), admin: User = Depends(require_roles(["admin"]))):
    case = db.query(KYCCase).get(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="KYC case not found")
    if body.status is not None:
        if body.status not in (KYCStatus.PENDING, KYCStatus.VERIFIED, KYCStatus.REJECTED):
            raise HTTPException(status_code=400, detail="Invalid status")
        case.status = body.status
    if body.notes is not None:
        case.notes = body.notes
    db.add(case)
    db.commit()
    db.refresh(case)
    write_audit(db, actor="admin", action="kyc_update", resource="kyc_cases", details=f"case_id={case.id},status={case.status}")
    return case
