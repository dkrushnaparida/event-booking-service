from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[str] = mapped_column(String, nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))

    status: Mapped[str] = mapped_column(default="CONFIRMED")

    event = relationship("Event", back_populates="bookings")
