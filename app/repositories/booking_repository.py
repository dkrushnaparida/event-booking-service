from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.booking import Booking


async def get_user_booking(db: AsyncSession, user_id: int, event_id: int):
    result = await db.execute(
        select(Booking).where(
            Booking.user_id == user_id,
            Booking.event_id == event_id,
            Booking.status == "CONFIRMED",
        )
    )
    return result.scalar_one_or_none()


async def create_booking(db: AsyncSession, user_id: int, event_id: int):
    booking = Booking(user_id=user_id, event_id=event_id, status="CONFIRMED")
    db.add(booking)
    await db.flush()
    return booking


async def get_booking_by_id_for_update(db: AsyncSession, booking_id: int):
    result = await db.execute(
        select(Booking).where(Booking.id == booking_id).with_for_update()
    )
    return result.scalar_one_or_none()


async def cancel_booking(db: AsyncSession, booking: Booking):
    booking.status = "CANCELLED"
    db.add(booking)
