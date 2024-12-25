from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class PayoutBase(BaseModel):
    bet_id: int
    user_id: int
    amount: Decimal = Field(..., description="Сумма выплаты (может быть отрицательной)")
    payout_date: Optional[datetime] = None


class PayoutCreate(PayoutBase):
    pass


class Payout(PayoutBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
