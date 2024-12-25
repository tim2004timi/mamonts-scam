from typing import List

from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from decimal import Decimal

from ..database import Base


class Bet(Base):
    __tablename__ = "bets"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"), nullable=False)
    win_team_id: Mapped[int] = mapped_column(Integer, ForeignKey("team.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    odds: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    bet_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="bets")
    event = relationship("Event", back_populates="bets")
    win_team = relationship("Team", back_populates="bets")
    payouts: Mapped[List["Payout"]] = relationship("Payout", back_populates="bet")
