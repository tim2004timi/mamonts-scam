from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import db_manager
from ..auth.dependencies import get_current_active_auth_user
from . import service
from .schemas import TeamsList, Team, TeamCreate, TeamUpdatePartial
from ..users import User

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    tags=["Teams"],
    prefix="/teams",
    dependencies=[
        Depends(http_bearer),
    ],
)


@router.get(
    path="/",
    response_model=TeamsList,
    summary="Получить список всех команд",
)
async def get_all_teams(
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
    page_size: int = 1000,
    page_number: int = 1,
):
    """
    Получает список всех команд.

    - **access_token**: Header bearer access token (required)

    - **page_size**: Количество команд на странице (по умолчанию=1000)
    - **page_number**: Номер страницы (по умолчанию=1)
    """
    return await service.get_all_teams(
        session=session,
        page_size=page_size,
        page_number=page_number,
    )


@router.get(
    path="/{team_id}/",
    response_model=Team,
    summary="Получить команду по ID",
)
async def get_team_by_id(
    team_id: int,
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
):
    """
    Получает команду по ID.

    - **access_token**: Header bearer access token (required)

    - **team_id**: ID команды (required)
    """
    return await service.get_team_by_id(session=session, team_id=team_id)


@router.post(
    path="/",
    response_model=Team,
    summary="Создать новую команду",
)
async def create_team(
    team_create: TeamCreate,
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
):
    """
    Создает новую команду.

    - **access_token**: Header bearer access token (required)

    - **team_name**: Название команды (required)
    - **squad_list**: Список состава команды (список строк)
    - **description**: Описание команды (optional)
    """
    return await service.create_team(session=session, team_create=team_create, user=user)


@router.patch(
    path="/{team_id}/",
    response_model=Team,
    summary="Обновить данные команды по ID",
)
async def update_team(
    team_id: int,
    team_update: TeamUpdatePartial,
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
):
    """
    Обновляет данные команды по ID.

    - **access_token**: Header bearer access token (required)

    - **team_id**: ID команды (required)
    - **team_name**: Название команды (optional)
    - **squad_list**: Список состава команды (список строк, optional)
    - **description**: Описание команды (optional)
    """
    team = await service.get_team_by_id(session=session, team_id=team_id)
    return await service.update_team(session=session, team=team, team_update=team_update, user=user)


@router.delete(
    path="/{team_id}/",
    response_model=Team,
    summary="Удалить команду по ID",
)
async def delete_team(
    team_id: int,
    session: AsyncSession = Depends(db_manager.session_dependency),
    user: User = Depends(get_current_active_auth_user),
):
    """
    Удаляет команду по ID.

    - **access_token**: Header bearer access token (required)

    - **team_id**: ID команды (required)
    """
    team = await service.get_team_by_id(session=session, team_id=team_id)
    await service.delete_team(session=session, team=team, user=user)
    return team
