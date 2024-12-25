from typing import List, Optional

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from ..database import Base


class Event(Base):
    __tablename__ = "events"

    event_name: Mapped[str] = mapped_column(String(100), nullable=False)
    event_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    event_end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ongoing")

    first_team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), nullable=False)
    second_team_id: Mapped[int] = mapped_column(ForeignKey("team.id"), nullable=False)

    first_team = relationship("Team", foreign_keys=[first_team_id])
    second_team = relationship("Team", foreign_keys=[second_team_id])

    current_odds: Mapped["CurrentOdds"] = relationship("CurrentOdds", uselist=False, back_populates="event")
    bets: Mapped[List["Bet"]] = relationship("Bet", back_populates="event")

    winning_team_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("team.id"), nullable=True)
    winning_team = relationship("Team", foreign_keys=[winning_team_id])
