from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import csv
import io

from app.api.deps import get_db
from app.schemas.business import BusinessCreate, BusinessRead
from app.crud.business import create_business, get_business
from app.core.deps import get_current_user
from app.db.models.user import User
from app.core.permissions import require_admin
from app.core.limiter import limiter

from app.worker.tasks import scrape_businesses 
from app.db.models.scrape_job import ScrapeJob
from app.db.models.business import Business
from fastapi.responses import StreamingResponse
from app.services.lead_scoring import calculate_lead_score
from app.services.serpapi_scraper import SerpAPIScraper
from app.core.config import settings

router = APIRouter(
    prefix="/businesses",
    tags=["Businesses"],
    dependencies=[Depends(get_current_user)])


@router.post("/")
@limiter.limit("20/minute")
def create_new_business(
    request: Request,
    business: BusinessCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    new_business = create_business(db, business, current_user.id)
    return new_business

@router.get("/export")
def export_businesses(
    job_id: int | None = None, # <--- ADD THIS
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Business).filter(Business.owner_id == current_user.id)
    
    if job_id:
        query = query.filter(Business.job_id == job_id)
        
    businesses = query.order_by(Business.lead_score.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "Name",
        "City",
        "Industry",
        "Phone",
        "Website",
        "Lead Score"
    ])

    # Rows
    for b in businesses:
        writer.writerow([
            b.name,
            b.city,
            b.industry,
            b.phone,
            b.website,
            b.lead_score
        ])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=businesses.csv"
        }
    )

@router.get("/{business_id}", response_model=BusinessRead)
def read_business(
    business_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)):

    business = get_business(db, business_id, current_user.id) 
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

@router.get("/")
def search(
    job_id: int | None = None,  
    city: str | None = None,
    industry: str | None = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    
    
    query = db.query(Business).filter(Business.owner_id == current_user.id)
    
    if job_id:
        query = query.filter(Business.job_id == job_id)
    if city:
        query = query.filter(Business.city.ilike(f"%{city}%"))
    if industry:
        query = query.filter(Business.industry.ilike(f"%{industry}%"))

    return query.order_by(Business.lead_score.desc()) \
    .limit(limit) \
    .offset(offset) \
    .all()


@router.delete("/{business_id}")
def delete_business(
    business_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)):
    return {"message": "Admin delete working"}


@router.post("/{business_id}/scrape")
def rescrape_business(
    business_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    business = db.query(Business).filter(
        Business.id == business_id,
        Business.owner_id == current_user.id
    ).first()

    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    if not business.place_id:
        raise HTTPException(status_code=400, detail="No place_id stored for this business")


    scraper = SerpAPIScraper(settings.SERPAPI_KEY)


    data = scraper.fetch_place_details(business.place_id)

    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch updated data")


    business.rating = data.get("rating")
    business.reviews = data.get("reviews")
    business.website = data.get("website")
    business.phone = data.get("phone")
    business.address = data.get("address")
    business.description = data.get("description")

    business.lead_score = calculate_lead_score(business)

    db.commit()
    db.refresh(business)

    return business


@router.post("/scrape")
def trigger_scrape(
    city: str,
    industry: str,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
):
    
    job = ScrapeJob(
        user_id=current_user.id,
        status="pending"
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    
    scrape_businesses.delay(city, industry, current_user.id, job.id)

    return {"job_id": job.id, "message": "Scrape started"}


