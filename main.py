import uvicorn
from fastapi import FastAPI
import logging

from routers import person
from models import Base
from database import engine
from config import API_HOST, API_PORT


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Task 4")

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

app.middleware("http")(log_requests)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


app.include_router(person.router, prefix="/persons", tags=["persons"])


if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT, reload=True)
