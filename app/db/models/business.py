from sqlalchemy import Float, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.database import Base 


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(String, index=True, nullable=True)
    name = Column(String(255), nullable=False, index=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="businesses")
    
    industry = Column(String(100), index=True)

    address = Column(Text)
    city = Column(String(100), index=True)

    phone = Column(String(50))
    email = Column(String(255))
    rating = Column(Float, nullable=True) 
    reviews = Column(Integer, nullable=True)

    website = Column(String(255), nullable=True)

    
    description = Column(Text, nullable=True)

    lead_score = Column(Integer, default=0)
    job_id = Column(Integer, ForeignKey("scrape_jobs.id"), nullable=True)
    job = relationship("ScrapeJob", back_populates="businesses")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
