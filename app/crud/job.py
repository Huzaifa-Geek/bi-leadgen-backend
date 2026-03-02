from sqlalchemy.orm import Session
from app.db.models.scrape_job import ScrapeJob


def get_job_by_id(db: Session, job_id: int):
    return db.query(ScrapeJob).filter(ScrapeJob.id == job_id).first()
