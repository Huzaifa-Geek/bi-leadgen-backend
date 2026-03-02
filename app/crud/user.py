from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.db.models.user import User
from app.core.security import hash_password, verify_password, pwd_context 

def create_user(db: Session, email: str, password: str):
    user = User(
        email=email,
        hashed_password=hash_password(password),
        role="user",
        is_active=True,
    )
    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    db.refresh(user)
    return user

def authenticate(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
   
    if pwd_context.needs_update(user.hashed_password):
        user.hashed_password = hash_password(password)
        db.add(user)
        db.commit()
        db.refresh(user)

    return user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()