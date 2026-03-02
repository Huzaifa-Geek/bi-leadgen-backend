from fastapi import FastAPI
from app.core.config import settings
from app.api.router import router as api_router 
from app.core.middleware import logging_middleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
from app.core.limiter import limiter

app = FastAPI(title=settings.APP_NAME, version="1.0.1")


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.add_middleware(SlowAPIMiddleware)
app.middleware("http")(logging_middleware)


app.include_router(api_router)



@app.get("/")
def root():
    return {"status": "ok"}
