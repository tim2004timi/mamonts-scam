from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import db_manager
from ..auth.dependencies import get_current_active_auth_user
from . import service
from .schemas import BetsList, Bet, BetCreate, BetUpdatePartial
from ..users import User

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    tags=["Bets"],
    prefix="/bets",
    dependencies=[
        Depends(http_bearer),
    ],
)


@router.get(
    path="/",
    response_model=BetsList,
    summary="Получить все ставки",
)
async def get_all_bets(
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
    page_size: int = 1000,
    page_number: int = 1,
):
    """
    Получает список всех ставок.

    - **access_token**: Header bearer access token (required)

    - **page_size**: Количество ставок на странице (по умолчанию=1000)
    - **page_number**: Номер страницы (по умолчанию=1)
    """
    return await service.get_all_bets(
        session=session,
        page_size=page_size,
        page_number=page_number,
    )


@router.get(
    path="/{bet_id}/",
    response_model=Bet,
    summary="Получить ставку по ID",
)
async def get_bet_by_id(
    bet_id: int,
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
):
    """
    Получает ставку по ID.

    - **access_token**: Header bearer access token (required)

    - **bet_id**: ID ставки (required)
    """
    return await service.get_bet_by_id(session=session, bet_id=bet_id)


@router.post(
    path="/",
    response_model=Bet,
    summary="Создать новую ставку",
)
async def create_bet(
    bet_create: BetCreate,
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
):
    """
    Создает новую ставку.

    - **access_token**: Header bearer access token (required)

    - **event_id**: ID события (required)
    - **win_team_id**: ID команды, на которую сделана ставка (required)
    - **amount**: Сумма ставки (required)
    """
    return await service.create_bet(session=session, bet_create=bet_create, user=user)


@router.patch(
    path="/{bet_id}/",
    response_model=Bet,
    summary="Обновить ставку по ID",
)
async def update_bet(
    bet_id: int,
    bet_update: BetUpdatePartial,
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
):
    """
    Обновляет ставку по ID.

    - **access_token**: Header bearer access token (required)

    - **bet_id**: ID ставки (required)
    - **status**: Новый статус ставки (optional)
    """
    bet = await service.get_bet_by_id(session=session, bet_id=bet_id)
    if bet.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к ставке",
        )
    return await service.update_bet(session=session, bet=bet, bet_update=bet_update, user=user)


@router.delete(
    path="/{bet_id}/",
    response_model=Bet,
    summary="Удалить ставку по ID",
)
async def delete_bet(
    bet_id: int,
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
):
    """
    Удаляет ставку по ID.

    - **access_token**: Header bearer access token (required)

    - **bet_id**: ID ставки (required)
    """
    bet = await service.get_bet_by_id(session=session, bet_id=bet_id)
    if bet.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к ставке",
        )
    await service.delete_bet(session=session, bet=bet, user=user)
    return bet
