from math import ceil
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import CurrentOdds
from .schemas import CurrentOddsCreate, CurrentOddsUpdate, CurrentOddsList
from ..events.models import Event
from ..users import User


async def get_all_current_odds(
    session: AsyncSession,
    page_size: int = 1000,
    page_number: int = 1,
) -> CurrentOddsList:
    stmt = select(CurrentOdds).order_by(CurrentOdds.id.desc())
    result = await session.execute(stmt)
    odds = list(result.scalars().all())

    limit = page_size
    offset = (page_number - 1) * page_size
    response_odds = odds[offset : offset + limit]
    total_pages = ceil(len(odds) / page_size) if page_size else 1
    odds_list = CurrentOddsList(
        odds=response_odds, total_pages=total_pages, current_page=page_number
    )
    return odds_list


async def get_current_odds_by_id(session: AsyncSession, odds_id: int) -> CurrentOdds:
    odds = await session.get(CurrentOdds, odds_id)
    if not odds:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Коэффициенты с ID ({odds_id}) не найдены",
        )
    return odds


async def create_current_odds(session: AsyncSession, odds_create: CurrentOddsCreate, user: User) -> CurrentOdds:
    stmt = select(CurrentOdds).where(CurrentOdds.event_id == odds_create.event_id)
    result = await session.execute(stmt)
    existing_odds = result.scalars().first()
    if existing_odds:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Коэффициенты для события с ID ({odds_create.event_id}) уже существуют",
        )

    event = await session.get(Event, odds_create.event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Событие с ID ({odds_create.event_id}) не найдено",
        )

    odds = CurrentOdds(**odds_create.model_dump())
    session.add(odds)
    await session.commit()
    await session.refresh(odds)
    return odds


async def update_current_odds(session: AsyncSession, odds: CurrentOdds, odds_update: CurrentOddsUpdate, user: User) -> CurrentOdds:
    for name, value in odds_update.model_dump(exclude_unset=True).items():
        setattr(odds, name, value)
    await session.commit()
    return odds


async def delete_current_odds(session: AsyncSession, odds: CurrentOdds, user: User) -> None:
    await session.delete(odds)
    await session.commit()
