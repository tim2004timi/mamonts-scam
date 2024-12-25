from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class TeamBase(BaseModel):
    team_name: str = Field(..., max_length=100)
    squad_list: Optional[List[str]] = []
    description: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class TeamUpdatePartial(BaseModel):
    team_name: Optional[str] = Field(None, max_length=100)
    squad_list: Optional[List[str]] = None
    description: Optional[str] = None


class Team(TeamBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TeamsList(BaseModel):
    teams: List[Team]
    total_pages: int
    current_page: int
