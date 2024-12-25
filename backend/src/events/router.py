from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import db_manager
from ..auth.dependencies import get_current_active_auth_user
from . import service
from .schemas import EventsList, Event, EventCreate, EventUpdate
from ..users.models import User

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    tags=["Events"],
    prefix="/events",
    dependencies=[
        Depends(http_bearer),
    ],
)


@router.get(
    path="/ongoing/",
    response_model=EventsList,
    summary="Получить все незавершенные события",
)
async def get_all_ongoing_events(
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
    page_size: int = 1000,
    page_number: int = 1,
):
    """
    Получает список всех незавершенных событий.

    - **access_token**: Header bearer access token (required)

    - **page_size**: Количество событий на странице (по умолчанию=1000)
    - **page_number**: Номер страницы (по умолчанию=1)
    """
    return await service.get_all_ongoing_events(
        session=session,
        page_size=page_size,
        page_number=page_number,
    )


@router.get(
    path="/{event_id}/",
    response_model=Event,
    summary="Получить событие по ID",
)
async def get_event_by_id(
    event_id: int,
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
):
    """
    Получает событие по ID.

    - **access_token**: Header bearer access token (required)

    - **event_id**: ID события (required)
    """
    return await service.get_event_by_id(session=session, event_id=event_id)


@router.post(
    path="/",
    response_model=Event,
    summary="Создать новое событие",
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    event_create: EventCreate,
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
):
    """
    Создает новое событие.

    - **access_token**: Header bearer access token (required)

    - **event_name**: Название события (required)
    - **event_date**: Дата и время события (required)
    - **event_type**: Тип события (required)
    - **first_team_id**: ID первой команды (required)
    - **second_team_id**: ID второй команды (required)
    """
    return await service.create_event(session=session, event_create=event_create, user=user)


@router.patch(
    path="/{event_id}/",
    response_model=Event,
    summary="Обновить событие по ID",
)
async def update_event(
    event_id: int,
    event_update: EventUpdate,
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
):
    """
    Обновляет событие по ID.

    - **access_token**: Header bearer access token (required)

    - **event_id**: ID события (required)
    - **event_end_date**: Дата и время завершения события (optional)
    - **winning_team_id**: ID победившей команды (optional)
    """
    return await service.update_event(session=session, event_id=event_id, event_update=event_update, user=user)
