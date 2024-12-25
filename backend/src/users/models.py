import random
from typing import List

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from ..database import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[bytes]
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    balance: Mapped[float] = mapped_column(default=0.0)
    active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    bets: Mapped[List["Bet"]] = relationship("Bet", back_populates="user")
    payouts: Mapped[List["Payout"]] = relationship("Payout", back_populates="user")

