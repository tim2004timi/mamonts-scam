from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import db_manager
from ..auth.dependencies import get_current_active_auth_user
from . import service
from .schemas import Payout, PayoutCreate

from ..users.models import User

router = APIRouter(
    tags=["Payouts"],
    prefix="/payouts",
    dependencies=[
        Depends(get_current_active_auth_user),
    ],
)


@router.get(
    path="/",
    response_model=List[Payout],
    summary="Получить все выплаты пользователя",
)
async def get_all_payouts(
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
):
    """
    Получает список всех выплат пользователя.

    - **access_token**: Header bearer access token (required)
    """
    return await service.get_all_payouts(session=session, user=user.id)


@router.get(
    path="/{payout_id}/",
    response_model=Payout,
    summary="Получить выплату по ID",
)
async def get_payout_by_id(
    payout_id: int,
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
):
    """
    Получает выплату по ID.

    - **access_token**: Header bearer access token (required)
    - **payout_id**: ID выплаты (required)
    """
    payout = await service.get_payout_by_id(session=session, payout_id=payout_id)
    if payout.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к выплате",
        )
    return payout


@router.post(
    path="/",
    response_model=Payout,
    summary="Создать выплату",
)
async def create_payout(
    payout_create: PayoutCreate,
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
):
    """
    Создает новую выплату.

    - **access_token**: Header bearer access token (required)
    - **bet_id**: ID ставки (required)
    - **user_id**: ID пользователя (required)
    - **amount**: Сумма выплаты (required)
    """
    if payout_create.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя создавать выплаты для других пользователей",
        )
    return await service.create_payout(session=session, payout_create=payout_create)
