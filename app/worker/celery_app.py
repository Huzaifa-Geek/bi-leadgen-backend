from celery import Celery
import app.db.base

celery_app = Celery(
    "leadgen_worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["app.worker.tasks"], 
)

celery_app.conf.task_routes = {
    "app.worker.tasks.*": {"queue": "celery"},
}

celery_app.conf.worker_prefetch_multiplier = 1
