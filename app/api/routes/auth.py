from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.auth import UserCreate, Token
from app.crud.user import create_user, authenticate
from app.core.jwt import create_access_token
from app.core.limiter import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, data.email, data.password)


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request,data: UserCreate, db: Session = Depends(get_db)):
    user = authenticate(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=str(user.id))
    return {"access_token": token}
