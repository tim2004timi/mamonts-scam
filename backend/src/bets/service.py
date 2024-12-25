from math import ceil
from typing import List
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Bet
from .schemas import BetCreate, BetUpdatePartial, BetsList
from ..users.models import User
from ..events.models import Event
from ..teams.models import Team
from ..current_odds.models import CurrentOdds
from datetime import datetime


async def get_all_bets(
    session: AsyncSession,
    page_size: int = 1000,
    page_number: int = 1,
) -> BetsList:
    stmt = select(Bet).order_by(Bet.id.desc()).options(
        selectinload(Bet.user),
        selectinload(Bet.event),
        selectinload(Bet.win_team),
    )
    result = await session.execute(stmt)
    bets = list(result.scalars().all())

    limit = page_size
    offset = (page_number - 1) * page_size
    response_bets = bets[offset : offset + limit]
    total_pages = ceil(len(bets) / page_size) if page_size else 1
    bets_list = BetsList(
        bets=response_bets, total_pages=total_pages, current_page=page_number
    )
    return bets_list


async def get_bet_by_id(session: AsyncSession, bet_id: int) -> Bet:
    stmt = select(Bet).where(Bet.id == bet_id).options(
        selectinload(Bet.user),
        selectinload(Bet.event),
        selectinload(Bet.win_team),
    )
    result = await session.execute(stmt)
    bet = result.scalars().first()
    if not bet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ставка с ID ({bet_id}) не найдена",
        )
    return bet


async def create_bet(session: AsyncSession, bet_create: BetCreate, user: User) -> Bet:
    event = await session.get(Event, bet_create.event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Событие с ID ({bet_create.event_id}) не найдено",
        )

    if bet_create.win_team_id not in [event.first_team_id, event.second_team_id]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Команда с ID ({bet_create.win_team_id}) не участвует в событии",
        )

    stmt = select(CurrentOdds).where(CurrentOdds.event_id == bet_create.event_id)
    result = await session.execute(stmt)
    current_odds = result.scalars().first()
    if not current_odds:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Коэффициенты для события с ID ({bet_create.event_id}) не найдены",
        )

    if bet_create.win_team_id == event.first_team_id:
        odds_value = current_odds.first_win_odds
    else:
        odds_value = current_odds.second_win_odds

    if odds_value <= Decimal('0'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недопустимый коэффициент для ставки",
        )

    bet = Bet(
        user_id=user.id,
        event_id=bet_create.event_id,
        win_team_id=bet_create.win_team_id,
        amount=bet_create.amount,
        odds=odds_value,
        bet_date=datetime.utcnow(),
    )
    session.add(bet)

    def recalculate_odds(current_odds: CurrentOdds, win_team_id: int, amount: Decimal):
        """
        Пересчитывает коэффициенты для выбранной команды.
        """
        adjustment_factor = (amount / Decimal('100.0')) * Decimal('0.01')  # 1% за каждые 100 единиц

        if win_team_id == event.first_team_id:
            new_first_win_odds = current_odds.first_win_odds * (Decimal('1') - adjustment_factor)
            new_first_win_odds = max(new_first_win_odds, Decimal('1.01'))
            current_odds.first_win_odds = new_first_win_odds.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            new_second_win_odds = current_odds.second_win_odds * (Decimal('1') - adjustment_factor)
            new_second_win_odds = max(new_second_win_odds, Decimal('1.01'))
            current_odds.second_win_odds = new_second_win_odds.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    recalculate_odds(current_odds, bet_create.win_team_id, bet_create.amount)

    await session.commit()
    await session.refresh(bet)

    stmt = select(Bet).where(Bet.id == bet.id).options(
        selectinload(Bet.user),
        selectinload(Bet.event),
        selectinload(Bet.win_team),
    )
    result = await session.execute(stmt)
    bet = result.scalars().first()

    return bet


async def update_bet(
    session: AsyncSession, bet: Bet, bet_update: BetUpdatePartial, user: User
) -> Bet:
    await session.commit()
    return bet


async def delete_bet(session: AsyncSession, bet: Bet, user: User) -> None:
    await session.delete(bet)
    await session.commit()
