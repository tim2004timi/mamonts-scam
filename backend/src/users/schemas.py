from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
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
    first_name: str
    last_name: str


class UserMeUpdatePartial(BaseModel):
    password: str | None = Field(
        default=None,
        min_length=3,
        max_length=16,
        pattern="^[A-Za-z0-9]+$",
    )


class LoginUser(BaseModel):
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


class User(UserBase):
    id: int
    username: str
    created_at: datetime
    active: bool
    first_name: str
    last_name: str
    model_config = ConfigDict(from_attributes=True)
