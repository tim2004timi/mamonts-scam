from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..database import Base


class CurrentOdds(Base):
    __tablename__ = "current_odds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"), unique=True, nullable=False)
    first_win_odds: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False)
    second_win_odds: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False)

    event: Mapped["Event"] = relationship("Event", back_populates="current_odds")
