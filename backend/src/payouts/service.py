from typing import List
from decimal import Decimal
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Payout
from .schemas import PayoutCreate, Payout
from ..users.models import User
from ..bets.models import Bet


async def get_all_payouts(session: AsyncSession, user: int) -> List[Payout]:
    stmt = select(Payout).where(Payout.user_id == user).order_by(Payout.payout_date.desc())
    result = await session.execute(stmt)
    payouts = result.scalars().all()
    return payouts


async def get_payout_by_id(session: AsyncSession, payout_id: int) -> Payout:
    stmt = select(Payout).where(Payout.id == payout_id)
    result = await session.execute(stmt)
    payout = result.scalars().first()
    if not payout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Выплата с ID ({payout_id}) не найдена",
        )
    return payout


async def create_payout(session: AsyncSession, payout_create: PayoutCreate) -> Payout:
    # Проверяем существование ставки
    stmt = select(Bet).where(Bet.id == payout_create.bet_id)
    result = await session.execute(stmt)
    bet = result.scalars().first()
    if not bet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ставка с ID ({payout_create.bet_id}) не найдена",
        )

    stmt = select(User).where(User.id == payout_create.user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с ID ({payout_create.user_id}) не найден",
        )

    payout = Payout(**payout_create.model_dump())
    payout.payout_date = payout_create.payout_date or datetime.utcnow()

    session.add(payout)
    await session.commit()
    await session.refresh(payout)
    return payout
