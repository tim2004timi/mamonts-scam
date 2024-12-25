from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from decimal import Decimal

from ..database import Base


class Payout(Base):
    __tablename__ = "payouts"

    bet_id: Mapped[int] = mapped_column(Integer, ForeignKey("bets.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    payout_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    bet = relationship("Bet", back_populates="payouts")
    user = relationship("User", back_populates="payouts")
