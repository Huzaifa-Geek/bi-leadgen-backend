from fastapi import APIRouter
from app.api.routes import auth, businesses, jobs

router = APIRouter()

router.include_router(auth.router)
router.include_router(businesses.router)
router.include_router(jobs.router)
