from app.worker.celery_app import celery_app
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud.business import create_business
from app.schemas.business import BusinessCreate
from app.db.models.scrape_job import ScrapeJob
from app.db.models.business import Business
from app.services.serpapi_scraper import SerpAPIScraper
import os
import time
from datetime import datetime

@celery_app.task(bind=True)
def scrape_businesses(self, city: str, industry: str, user_id: int, job_id: int):
    with SessionLocal() as db:
        job = db.get(ScrapeJob, job_id)
        if not job:
            return {"status": "error", "message": "Job not found"}

        try:
            job.status = "processing"
            job.started_at = datetime.utcnow()
            db.commit()

            api_key = os.getenv("SERPAPI_KEY")
            scraper = SerpAPIScraper(api_key)

            page = 0
            MAX_PAGES = 5  
            created_count = 0
            has_more = True

            while has_more and page < MAX_PAGES:
                batch = scraper.fetch_page(city, industry, page)

                if not batch:
                    has_more = False
                    break


                for item in batch:
                    existing = db.query(Business).filter(
                        Business.place_id == item.get("place_id"),
                        Business.owner_id == user_id
                    ).first()

                    if existing:
                        continue

                    try:
                        item["job_id"] = job_id
                        business_data = BusinessCreate(**item)
                        create_business(db, business_data, user_id)
                        created_count += 1
                    except Exception as e:
                        print(f"Error preparing {item.get('name')}: {e}")
                        db.rollback() 


                job.result_count = created_count
                db.commit() 
                
                page += 1
                time.sleep(1.5)

            job.status = "completed"
            job.completed_at = datetime.utcnow()
            db.commit()

            return {"status": "completed", "count": created_count}

        except Exception as e:
            db.rollback()
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()
            db.commit()
            raise e

