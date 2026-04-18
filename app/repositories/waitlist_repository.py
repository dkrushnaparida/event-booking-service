from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.waitlist import Waitlist


async def add_to_waitlist(db: AsyncSession, user_id: int, event_id: int):
    wait = Waitlist(user_id=user_id, event_id=event_id)
    db.add(wait)
    return wait


async def get_next_waitlist_user(db: AsyncSession, event_id: int):
    result = await db.execute(
        select(Waitlist)
        .where(Waitlist.event_id == event_id)
        .order_by(Waitlist.created_at)  # FIFO
        .with_for_update(skip_locked=True)
        .limit(1)
    )
    return result.scalar_one_or_none()


async def remove_from_waitlist(db: AsyncSession, waitlist_entry: Waitlist):
    await db.delete(waitlist_entry)
