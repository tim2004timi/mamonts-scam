from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import db_manager
from ..auth.dependencies import get_current_active_auth_user
from . import service
from .schemas import EventsList, Event
from ..users import User

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
    summary="Get all ongoing events",
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
    summary="Get event by id",
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
