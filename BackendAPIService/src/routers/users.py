from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.core.security import require_roles, get_password_hash
from src.models.user import User
from src.schemas.user import UserCreate, UserOut, UserUpdate
from src.utils.audit import write_audit

router = APIRouter()


@router.post("/", response_model=UserOut, summary="Create user", description="Create a new user (admin only).")
def create_user(user_in: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_roles(["admin"]))):
    if db.query(User).filter((User.username == user_in.username) | (User.email == user_in.email)).first():
        raise HTTPException(status_code=400, detail="Username or email already exists")
    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        is_active=True,
        roles="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    write_audit(db, actor="admin", action="user_create", resource="users", details=f"user_id={user.id}")
    return user


@router.get("/", response_model=List[UserOut], summary="List users", description="List all users (admin only).")
def list_users(db: Session = Depends(get_db), _: User = Depends(require_roles(["admin"]))):
    return db.query(User).order_by(User.id.desc()).all()


@router.get("/{user_id}", response_model=UserOut, summary="Get user", description="Get a user by ID (admin only).")
def get_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(["admin"]))):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut, summary="Update user", description="Update a user (admin only).")
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(["admin"]))):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_in.email is not None:
        user.email = user_in.email
    if user_in.password is not None:
        user.hashed_password = get_password_hash(user_in.password)
    if user_in.is_active is not None:
        user.is_active = user_in.is_active
    if user_in.roles is not None:
        user.roles = user_in.roles
    db.add(user)
    db.commit()
    db.refresh(user)
    write_audit(db, actor="admin", action="user_update", resource="users", details=f"user_id={user.id}")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user", description="Delete a user (admin only).")
def delete_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(["admin"]))):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    write_audit(db, actor="admin", action="user_delete", resource="users", details=f"user_id={user_id}")
    return None
