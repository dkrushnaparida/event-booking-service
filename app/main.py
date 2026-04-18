from fastapi import FastAPI
from app.core.config import settings
from app.db.session import engine

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(lambda conn: None)

@app.get("/")
async def root():
    return {"message": "Event Booking Service is running!"}
