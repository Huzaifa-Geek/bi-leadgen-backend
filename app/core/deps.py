from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.api.deps import get_db
from app.db.models.user import User
from app.crud.user import get_user_by_id



security = HTTPBearer(auto_error=True)


def get_current_user(
    
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    
    token = credentials.credentials

    try:
        payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )

        user_id: str | None = payload.get("sub")
        
        if payload.get("type") != "access":
            raise credentials_exception

        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_id(db, user_id=int(user_id))
    if not user:
        raise credentials_exception

    return user