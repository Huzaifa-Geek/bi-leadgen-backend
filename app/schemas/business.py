from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional


class BusinessBase(BaseModel):
    name: str = Field(..., min_length=2)
    industry: str = Field(..., min_length=2)
    city: str = Field(..., min_length=2)
    email: Optional[EmailStr]
    place_id: str | None = None
    
    @validator("*")
    def no_default_string(cls, v):
        if v == "string":
            raise ValueError("Invalid value")
        return v
    
class BusinessCreate(BusinessBase):
    pass


class BusinessRead(BusinessBase):
    id: int
    created_at: datetime
    address: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    description: Optional[str]
    rating: Optional[float]
    reviews: Optional[int]
    lead_score: Optional[float]

    class Config:
        from_attributes = True 
