from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JobStatusResponse(BaseModel):
    id: int
    status: str
    result_count: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True 
