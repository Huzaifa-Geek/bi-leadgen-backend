from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_db 
from app.crud.job import get_job_by_id
from app.schemas.job import JobStatusResponse

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("/{job_id}", response_model=JobStatusResponse)
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    
    job = get_job_by_id(db, job_id)

    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    
    if job.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this job")

    return job
