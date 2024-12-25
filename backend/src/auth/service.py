from fastapi import Depends

from .dependencies import validate_auth_user_body
from ..users.schemas import User as UserSchema


async def login(user: UserSchema = Depends(validate_auth_user_body)):
    return user

