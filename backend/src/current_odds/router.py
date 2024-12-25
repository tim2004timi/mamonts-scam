from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import db_manager
from ..auth.dependencies import get_current_active_auth_user
from . import service
from .schemas import CurrentOdds, CurrentOddsCreate, CurrentOddsUpdate, CurrentOddsList
from ..users import User

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    tags=["Current Odds"],
    prefix="/odds",
    dependencies=[
        Depends(http_bearer),
    ],
)


@router.get(
    path="/",
    response_model=CurrentOddsList,
    summary="Получить все текущие коэффициенты",
)
async def get_all_current_odds(
        session: AsyncSession = Depends(db_manager.session_dependency),
        user: User = Depends(get_current_active_auth_user),
        page_size: int = 1000,
        page_number: int = 1,
):
    """
    Получает список всех текущих коэффициентов.

    - **access_token**: Header bearer access token (required)

    - **page_size**: Количество коэффициентов на странице (по умолчанию=1000)
    - **page_number**: Номер страницы (по умолчанию=1)
    """
    return await service.get_all_current_odds(
        session=session,
        page_size=page_size,
        page_number=page_number,
    )


@router.get(
    path="/{odds_id}/",
    response_model=CurrentOdds,
    summary="Получить коэффициенты по ID",
)
async def get_current_odds_by_id(
        odds_id: int,
        session: AsyncSession = Depends(db_manager.session_dependency),
        user: User = Depends(get_current_active_auth_user),
):
    """
    Получает текущие коэффициенты по ID.

    - **access_token**: Header bearer access token (required)

    - **odds_id**: ID коэффициентов (required)
    """
    return await service.get_current_odds_by_id(session=session, odds_id=odds_id)


@router.post(
    path="/",
    response_model=CurrentOdds,
    summary="Создать текущие коэффициенты",
)
async def create_current_odds(
        odds_create: CurrentOddsCreate,
        session: AsyncSession = Depends(db_manager.session_dependency),
        user: User = Depends(get_current_active_auth_user),
):
    """
    Создает текущие коэффициенты для события.

    - **access_token**: Header bearer access token (required)

    - **event_id**: ID события (required)
    - **first_win_odds**: Коэффициент на победу первой команды (required)
    - **second_win_odds**: Коэффициент на победу второй команды (required)
    """
    return await service.create_current_odds(session=session, odds_create=odds_create, user=user)


@router.patch(
    path="/{odds_id}/",
    response_model=CurrentOdds,
    summary="Обновить текущие коэффициенты",
)
async def update_current_odds(
        odds_id: int,
        odds_update: CurrentOddsUpdate,
        session: AsyncSession = Depends(db_manager.session_dependency),
        user: User = Depends(get_current_active_auth_user),
):
    """
    Обновляет текущие коэффициенты по ID.

    - **access_token**: Header bearer access token (required)

    - **odds_id**: ID коэффициентов (required)
    - **first_win_odds**: Коэффициент на победу первой команды (optional)
    - **second_win_odds**: Коэффициент на победу второй команды (optional)
    """
    odds = await service.get_current_odds_by_id(session=session, odds_id=odds_id)
    return await service.update_current_odds(session=session, odds=odds, odds_update=odds_update, user=user)


@router.delete(
    path="/{odds_id}/",
    response_model=CurrentOdds,
    summary="Удалить текущие коэффициенты",
)
async def delete_current_odds(
        odds_id: int,
        session: AsyncSession = Depends(db_manager.session_dependency),
        user: User = Depends(get_current_active_auth_user),
):
    """
    Удаляет текущие коэффициенты по ID.

    - **access_token**: Header bearer access token (required)

    - **odds_id**: ID коэффициентов (required)
    """
    odds = await service.get_current_odds_by_id(session=session, odds_id=odds_id)
    await service.delete_current_odds(session=session, odds=odds, user=user)
    return odds
