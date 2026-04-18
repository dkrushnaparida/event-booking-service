from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.booking_service import BookingService
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post("/book")
async def book_event(user_id: str, event_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await BookingService.book_event(db, user_id, event_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
