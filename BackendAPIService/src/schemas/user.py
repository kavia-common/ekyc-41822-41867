from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(..., description="Unique username")
    email: EmailStr = Field(..., description="User email")
    is_active: bool = Field(default=True, description="Active status")
    roles: str = Field(default="user", description="Comma separated roles")


class UserCreate(BaseModel):
    username: str = Field(..., description="Unique username")
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="Plain password")


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="User email")
    password: Optional[str] = Field(None, description="New password")
    is_active: Optional[bool] = Field(None, description="Active status")
    roles: Optional[str] = Field(None, description="Comma separated roles")


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    roles: str

    class Config:
        from_attributes = True
