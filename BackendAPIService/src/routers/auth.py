from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.db import get_db
from src.core.security import authenticate_user, create_access_token, get_current_user
from src.schemas.auth import Token
from src.schemas.user import UserOut
from src.utils.audit import write_audit
from src.models.user import User

router = APIRouter()


@router.post(
    "/token",
    response_model=Token,
    summary="Obtain JWT access token",
    description="Use username and password to obtain a JWT access token.",
)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        write_audit(db, actor=form_data.username, action="auth_failed", resource="auth", details="Invalid credentials")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": user.username, "roles": user.roles.split(",")}, expires_delta=access_token_expires)
    write_audit(db, actor=user.username, action="auth_success", resource="auth", details="Issued token")
    return {"access_token": token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get current user profile",
    description="Retrieve the profile of the authenticated user.",
)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
