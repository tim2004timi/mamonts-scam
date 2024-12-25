# events/service.py
from math import ceil
from typing import List, Optional
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Event
from .schemas import EventsList, EventCreate, EventUpdate
from ..users.models import User
from ..bets.models import Bet
from ..payouts.models import Payout
from datetime import datetime

from ..payouts.service import create_payout


async def get_all_ongoing_events(
    session: AsyncSession,
    page_size: int = 1000,
    page_number: int = 1,
) -> EventsList:
    stmt = (
        select(Event)
        .options(selectinload(Event.first_team),
                 selectinload(Event.second_team),
                 selectinload(Event.current_odds),
                 selectinload(Event.bets).selectinload(Bet.user))
        .where(Event.status != "completed")
        .order_by(Event.id.desc())
    )
    result = await session.execute(stmt)
    events = list(result.scalars().all())

    limit = page_size
    offset = (page_number - 1) * page_size
    response_events = events[offset: offset + limit]
    total_pages = ceil(len(events) / page_size) if page_size else 1
    events_list = EventsList(
        events=response_events, total_pages=total_pages, current_page=page_number
    )
    return events_list


async def get_event_by_id(session: AsyncSession, event_id: int) -> Event:
    stmt = (
        select(Event)
        .options(
            selectinload(Event.first_team),
            selectinload(Event.second_team),
            selectinload(Event.current_odds),
            selectinload(Event.bets).selectinload(Bet.user)
        )
        .where(Event.id == event_id)
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
) -> Event:
    event = Event(**event_create.model_dump())
    event.status = "ongoing"  # Устанавливаем статус по умолчанию
    session.add(event)
    await session.commit()
    await session.refresh(event)
    return event


async def update_event(
    session: AsyncSession, event_id: int, event_update: EventUpdate, user: User
) -> Event:
    event = await get_event_by_id(session, event_id)

    if event_update.event_end_date:
        event.event_end_date = event_update.event_end_date

    if event_update.winning_team_id:
        # Проверяем, что winning_team_id относится к одной из команд в событии
        if event_update.winning_team_id not in [event.first_team_id, event.second_team_id]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Команда с ID ({event_update.winning_team_id}) не участвует в событии",
            )
        event.winning_team_id = event_update.winning_team_id
        event.status = "completed"

    session.add(event)
    await session.commit()
    await session.refresh(event)

    if event.status == "completed":
        # Обработка выплат
        await process_payouts(session, event)

    return event


async def process_payouts(session: AsyncSession, event: Event) -> None:
    """
    Обрабатывает выплаты для всех ставок на завершённое событие.
    """
    # Получаем все ставки на это событие
    stmt = select(Bet).where(Bet.event_id == event.id).options(selectinload(Bet.user))
    result = await session.execute(stmt)
    bets = result.scalars().all()

    # Определяем победившую команду
    winning_team_id = event.winning_team_id
    if not winning_team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Winning team not set for event {event.id}",
        )

    for bet in bets:
        if bet.win_team_id == winning_team_id:
            # Выигрышная ставка
            payout_amount = bet.amount * bet.odds - bet.amount  # Чистый выигрыш
        else:
            # Проигрышная ставка
            payout_amount = -bet.amount  # Потеря суммы ставки

        # Создаём запись о выплате
        payout = Payout(
            bet_id=bet.id,
            user_id=bet.user_id,
            amount=payout_amount,
            payout_date=datetime.utcnow(),
        )
        session.add(payout)

        # Обновляем баланс пользователя
        bet_user = bet.user
        bet_user.balance += payout_amount  # Предполагается, что у модели User есть поле balance
        session.add(bet_user)

    await session.commit()
