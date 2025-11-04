from datetime import datetime, timedelta, timezone
from typing import Optional, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.db import get_db
from src.models.user import User
from src.schemas.auth import TokenData

# OAuth2PasswordBearer expects a tokenUrl for docs; we use /api/auth/token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")  # subject stores username
        if username is None:
            raise credentials_exception
        token_data = TokenData(sub=username, roles=payload.get("roles", []))
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, token_data.sub)
    if user is None or not user.is_active:
        raise credentials_exception
    return user


def require_roles(required_roles: List[str]):
    """Dependency factory to require at least one of the roles for access."""

    def _checker(current_user: User = Depends(get_current_user)) -> User:
        if not current_user.roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        user_roles = set([r.strip() for r in current_user.roles.split(",") if r.strip()])
        if not user_roles.intersection(set(required_roles)):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user

    return _checker


def create_default_admin_if_missing():
    """Create a default admin if no users exist. The password must be changed via admin API."""
    from src.core.db import SessionLocal
    db = SessionLocal()
    try:
        has_any_user = db.query(User).first()
        if has_any_user:
            return
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            roles="admin",
        )
        db.add(admin)
        db.commit()
    finally:
        db.close()
