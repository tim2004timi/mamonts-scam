from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

from ..teams.schemas import Team
from ..payouts.schemas import Payout
from ..current_odds.schemas import CurrentOdds
from ..bets.schemas import Bet


class EventBase(BaseModel):
    event_name: str
    event_date: datetime
    event_type: str


class EventCreate(EventBase):
    first_team_id: int
    second_team_id: int


class EventUpdate(BaseModel):
    event_end_date: Optional[datetime] = None
    winning_team_id: Optional[int] = None


class Event(EventBase):
    id: int
    event_end_date: Optional[datetime]
    status: str
    first_team: Optional[Team]
    second_team: Optional[Team]
    current_odds: Optional["CurrentOdds"]
    bets: Optional[List["Bet"]]

    model_config = ConfigDict(from_attributes=True)


class EventsList(BaseModel):
    events: List[Event]
    total_pages: int
    current_page: int
