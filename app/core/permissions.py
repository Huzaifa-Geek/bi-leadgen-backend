from fastapi import Depends, HTTPException, status
from app.core.deps import get_current_user
from app.db.models.user import User


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user
