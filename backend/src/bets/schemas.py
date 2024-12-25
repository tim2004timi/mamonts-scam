from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

from ..users.schemas import User
# from ..events.schemas import Event
from ..teams.schemas import Team


class BetBase(BaseModel):
    user_id: int
    event_id: int
    win_team_id: int
    amount: Decimal = Field(..., ge=0)
    odds: Decimal = Field(..., ge=0)


class BetCreate(BaseModel):
    event_id: int
    win_team_id: int
    amount: Decimal = Field(..., ge=0)


class BetUpdatePartial(BaseModel):
    pass


class Bet(BetBase):
    id: int
    bet_date: datetime
    win_team: Optional[Team] = None

    model_config = ConfigDict(from_attributes=True)


class BetsList(BaseModel):
    bets: list[Bet]
    total_pages: int
    current_page: int
