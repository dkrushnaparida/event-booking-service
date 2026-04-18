from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event import Event


async def get_event_for_update(db: AsyncSession, event_id: int) -> Event | None:
    result = await db.execute(
        select(Event).where(Event.id == event_id).with_for_update()
    )
    return result.scalar_one_or_none()


async def increment_seat(event: Event):
    event.available_seats += 1


async def decrement_seat(event: Event):
    event.available_seats -= 1
