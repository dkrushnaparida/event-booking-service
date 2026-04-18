from sqlalchemy.ext.asyncio import AsyncSession
from app.models.waitlist import Waitlist
from sqlalchemy import select


async def add_to_waitlist(db: AsyncSession, user_id: int, event_id: int):
    wait = Waitlist(user_id=user_id, event_id=event_id)
    db.add(wait)
    return wait


async def get_next_waitlist_user(db: AsyncSession, event_id: int):
    result = await db.execute(
        select(Waitlist)
        .where(Waitlist.event_id == event_id)
        .order_by(Waitlist.created_at)
        .limit(1)
        .with_for_update()
    )

    return result.scalar_one_or_none()
