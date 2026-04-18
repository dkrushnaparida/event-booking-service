from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.booking_service import BookingService
from app.db import get_db

router = APIRouter()
service = BookingService()


@router.post("/cancel/{booking_id}")
async def cancel_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await service.cancel_booking(db, booking_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
