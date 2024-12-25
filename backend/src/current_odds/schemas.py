from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CurrentOddsBase(BaseModel):
    event_id: int
    first_win_odds: float = Field(..., ge=0)
    second_win_odds: float = Field(..., ge=0)


class CurrentOddsCreate(CurrentOddsBase):
    pass


class CurrentOddsUpdate(BaseModel):
    first_win_odds: Optional[float] = Field(None, ge=0)
    second_win_odds: Optional[float] = Field(None, ge=0)


class CurrentOdds(CurrentOddsBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CurrentOddsList(BaseModel):
    odds: list[CurrentOdds]
    total_pages: int
    current_page: int
