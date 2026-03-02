from datetime import datetime, timedelta
from jose import jwt

from app.core.config import settings


def create_access_token(subject: str):
    expire = datetime.utcnow() + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES
    )
    payload = {
        "sub": subject,
        "exp": expire,
        "type": "access"
    }
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
