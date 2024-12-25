from sqlalchemy import Column, Integer, String, Text, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

from ..database import Base


class Team(Base):
    __tablename__ = "team"

    team_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    squad_list: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    first_team_events = relationship(
        "Event",
        foreign_keys="[Event.first_team_id]",
        back_populates="first_team",
    )
    second_team_events = relationship(
        "Event",
        foreign_keys="[Event.second_team_id]",
        back_populates="second_team",
    )
    bets: Mapped[List["Bet"]] = relationship("Bet", back_populates="win_team")

