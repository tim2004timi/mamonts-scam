from math import ceil
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Team
from .schemas import TeamsList, TeamCreate, TeamUpdatePartial
from ..users import User


async def get_all_teams(
    session: AsyncSession,
    page_size: int = 1000,
    page_number: int = 1,
) -> TeamsList:
    stmt = select(Team).order_by(Team.id.desc())
    result = await session.execute(stmt)
    teams = result.scalars().all()

    limit = page_size
    offset = (page_number - 1) * page_size
    response_teams = teams[offset : offset + limit]
    total_pages = ceil(len(teams) / page_size)
    teams_list = TeamsList(
        teams=response_teams, total_pages=total_pages, current_page=page_number
    )
    return teams_list


async def get_team_by_id(session: AsyncSession, team_id: int) -> Team:
    team = await session.get(Team, team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Команда с ID ({team_id}) не найдена",
        )
    return team


async def create_team(session: AsyncSession, team_create: TeamCreate, user: User) -> Team:
    # Проверяем уникальность названия команды
    stmt = select(Team).where(Team.team_name == team_create.team_name)
    result = await session.execute(stmt)
    existing_team = result.scalars().first()
    if existing_team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Команда с названием '{team_create.team_name}' уже существует",
        )

    team = Team(**team_create.model_dump())
    session.add(team)
    await session.commit()
    await session.refresh(team)
    return team


async def update_team(
    session: AsyncSession, team: Team, team_update: TeamUpdatePartial, user: User
) -> Team:
    for name, value in team_update.model_dump(exclude_unset=True).items():
        setattr(team, name, value)
    await session.commit()
    return team


async def delete_team(session: AsyncSession, team: Team, user: User) -> None:
    await session.delete(team)
    await session.commit()
