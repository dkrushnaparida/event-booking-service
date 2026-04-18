from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.event_repository import get_event_for_update
from app.repositories.booking_repository import get_user_booking, create_booking
from app.repositories.waitlist_repository import add_to_waitlist


class BookingService:
    @staticmethod
    async def book_event(db: AsyncSession, user_id: int, event_id: int):
        async with db.begin():
            event = await get_event_for_update(db, event_id)
            if not event:
                raise ValueError("Event Not Found")

            existing = await get_user_booking(db, user_id, event_id)
            if existing:
                raise ValueError("User already has a booking for this event")

            if event.available_seats > 0:
                event.available_seats -= 1

                booking = await create_booking(db, user_id, event_id)

                return {
                    "status": "Booked",
                    "booking_id": booking.id,
                }

            await add_to_waitlist(db, user_id, event_id)

            return {
                "status": "Waitlisted",
            }
