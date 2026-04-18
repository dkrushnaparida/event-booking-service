from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.event_repository import get_event_for_update
from app.repositories.booking_repository import (
    get_user_booking,
    create_booking,
    get_booking_by_id_for_update,
    cancel_booking,
)
from app.repositories.waitlist_repository import (
    add_to_waitlist,
    get_next_waitlist_user,
    remove_from_waitlist,
)


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

    @staticmethod
    async def cancel_booking(db: AsyncSession, booking_id: int):
        async with db.begin():

            # booking with lock
            booking = await get_booking_by_id_for_update(db, booking_id)

            if not booking:
                raise ValueError("Booking Not Found")

            if booking.status != "CONFIRMED":
                raise ValueError("Booking already cancelled")

            # Lock the event row
            event = await get_event_for_update(db, booking.event_id)
            if not event:
                raise ValueError("Event Not Found")

            # Cancel booking
            await cancel_booking(db, booking)

            # Increase seat
            event.available_seats += 1

            # Fetch next waitlist user (FIFO)
            waitlist_entry = await get_next_waitlist_user(db, event.id)

            if waitlist_entry:
                # Create booking for that user
                new_booking = await create_booking(
                    db,
                    user_id=waitlist_entry.user_id,
                    event_id=event.id,
                )

                # Remove from waitlist
                await remove_from_waitlist(db, waitlist_entry)

                # Decrease seat again
                event.available_seats -= 1

                return {
                    "status": "Cancelled + Reassigned",
                    "booking_id": booking_id,
                    "new_booking_id": new_booking.id,
                }

            return {
                "status": "Cancelled",
                "booking_id": booking_id,
                "new_booking_id": None,
            }
