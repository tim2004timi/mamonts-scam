from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPBearer

from ..auth.dependencies import get_current_active_auth_user
from .schemas import User

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    tags=["Users"],
    prefix="/users",
    dependencies=[
        Depends(http_bearer),
    ],
)


@router.get(
    path="/me/",
    response_model=User,
    description="Get current auth user",
)
async def get_current_auth_user(user: User = Depends(get_current_active_auth_user)):
    return user


