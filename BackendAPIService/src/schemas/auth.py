from typing import List
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")


class TokenData(BaseModel):
    sub: str = Field(..., description="Subject (username)")
    roles: List[str] = Field(default_factory=list, description="Roles within token")


class LoginRequest(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")
