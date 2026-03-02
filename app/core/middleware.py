import time
from fastapi import Request


async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = round((time.time() - start_time) * 1000, 2)

    print(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"time={duration}ms"
    )

    return response
