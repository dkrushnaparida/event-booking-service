from app.db.base import Base
from app.models import event, booking, waitlist


async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
