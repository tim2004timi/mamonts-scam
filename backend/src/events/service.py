# event/service.py
from math import ceil
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Event as EventModel
from .schemas import EventsList, EventCreate
from ..users import User


async def get_all_ongoing_events(
    session: AsyncSession,
    page_size: int = 1000,
    page_number: int = 1,
) -> EventsList:
    stmt = (
        select(EventModel)
        .options(selectinload(EventModel.first_team), selectinload(EventModel.second_team))
        .where(EventModel.status != "completed")
        .order_by(EventModel.id.desc())
    )
    result = await session.execute(stmt)
    events = list(result.scalars().all())

    limit = page_size
    offset = (page_number - 1) * page_size
    response_events = events[offset : offset + limit]
    total_pages = ceil(len(events) / page_size)
    events_list = EventsList(
        events=response_events, total_pages=total_pages, current_page=page_number
    )
    return events_list


async def get_event_by_id(session: AsyncSession, event_id: int) -> EventModel:
    stmt = (
        select(EventModel)
        .options(selectinload(EventModel.first_team), selectinload(EventModel.second_team))
        .where(EventModel.id == event_id)
    )
    result = await session.execute(stmt)
    event = result.scalars().first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Событие с ID ({event_id}) не найдено",
        )
    return event


async def create_event(
    session: AsyncSession, event_create: EventCreate, user: User
) -> EventModel:
    event = EventModel(**event_create.model_dump())
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event
