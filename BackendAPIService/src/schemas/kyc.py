from typing import Optional
from pydantic import BaseModel, Field


class KYCBase(BaseModel):
    full_name: str = Field(..., description="Full legal name")
    document_type: str = Field(..., description="Document type, e.g., passport")
    document_number: str = Field(..., description="Document number")
    notes: Optional[str] = Field(None, description="Additional information")


class KYCCreate(KYCBase):
    pass


class KYCUpdate(BaseModel):
    status: Optional[str] = Field(None, description="KYC status")
    notes: Optional[str] = Field(None, description="Notes")


class KYCOut(BaseModel):
    id: int
    user_id: int
    full_name: str
    document_type: str
    document_number: str
    document_file_path: Optional[str]
    selfie_file_path: Optional[str]
    status: str
    notes: Optional[str]

    class Config:
        from_attributes = True
