from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from ..teams.schemas import Team


class EventBase(BaseModel):
    event_name: str
    event_date: datetime
    event_end_date: datetime | None
    event_type: str
    status: str
    first_team_id: int
    second_team_id: int


class EventCreate(EventBase):
    pass


class EventUpdatePartial(BaseModel):
    event_name: Optional[str] = None
    event_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    event_type: Optional[str] = None
    status: Optional[str] = None
    first_team_id: Optional[int] = None
    second_team_id: Optional[int] = None


class Event(EventBase):
    id: int
    first_team: Team
    second_team: Team

    model_config = ConfigDict(from_attributes=True)


class EventsList(BaseModel):
    events: list[Event]
    total_pages: int
    current_page: int
