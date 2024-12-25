from pydantic import BaseModel, Field

from src.config import auth_settings


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class LoginRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=12,
        pattern="^[a-z0-9]+$",
    )
    password: str = Field(
        ...,
        min_length=3,
        max_length=16,
        pattern="^[A-Za-z0-9]+$",
    )


