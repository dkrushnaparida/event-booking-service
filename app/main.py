from fastapi import FastAPI
from app.core.config import settings
from app.db.session import engine
from app.db.init_db import init_db

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
async def startup():
    await init_db(engine)


@app.get("/")
async def root():
    return {"message": "Event Booking Service is running!"}
