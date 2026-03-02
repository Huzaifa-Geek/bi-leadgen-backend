from sqlalchemy.orm import Session
from app.db.models.business import Business
from app.schemas.business import BusinessCreate
from typing import Any
from app.services.lead_scoring import calculate_lead_score

def create_business(db: Session, business: BusinessCreate, owner_id: int):
    place_id = getattr(business, "place_id", None)

    query = db.query(Business).filter(Business.owner_id == owner_id)
    if place_id:
        existing = query.filter(Business.place_id == place_id).first()
    else:
        existing = query.filter(
            Business.name == business.name,
            Business.city == business.city
        ).first()

    if existing:
        return existing  

   
    db_business = Business(
        name=business.name,
        city=business.city,
        industry=business.industry,
        owner_id=owner_id,
        
        place_id=getattr(business, "place_id", None),
        job_id=getattr(business, "job_id", None),
        address=getattr(business, "address", None),
        phone=getattr(business, "phone", None),
        website=getattr(business, "website", None),
        description=getattr(business, "description", None),
        rating=getattr(business, "rating", None),
        reviews=getattr(business, "reviews", None)
    )

    db_business.lead_score = calculate_lead_score(db_business)
    db.add(db_business)
    db.commit()
    db.refresh(db_business)

    return db_business


def get_business(db, business_id, owner_id):
    return db.query(Business).filter(
        Business.id == business_id,
        Business.owner_id == owner_id
    ).first()

def search_businesses(db, city=None, industry=None,
                      limit=20, offset=0,
                      owner_id=None):

    query = db.query(Business)

    if owner_id:
        query = query.filter(Business.owner_id == owner_id)

    if city:
        query = query.filter(Business.city == city)

    if industry:
        query = query.filter(Business.industry == industry)

    return query.order_by(Business.lead_score.desc()) \
            .offset(offset) \
            .limit(limit) \
            .all()