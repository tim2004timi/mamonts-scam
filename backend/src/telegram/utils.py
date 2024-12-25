import json
from datetime import datetime
from enum import Enum
from itertools import zip_longest

import pytz
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from functools import wraps
from fastapi import HTTPException

from src.telegram.keyboards import menu_reply_keyboard


class Permission(Enum):
    ADMIN = 1
    ALL = 2


async def answer_deny(event, message: str) -> None:
    if isinstance(event, CallbackQuery):
        await event.message.answer(message, reply_markup=menu_reply_keyboard)
        await event.answer()
    elif isinstance(event, Message):
        await event.answer(message, reply_markup=menu_reply_keyboard)


def delete_and_send_new_message(func):
    @wraps(func)
    async def wrapper(callback: CallbackQuery, *args, **kwargs):
        await callback.message.delete()
        await func(callback, *args, **kwargs)
        await callback.answer()

    return wrapper


def edit_message(func):
    @wraps(func)
    async def wrapper(callback: CallbackQuery, *args, **kwargs):
        # Вызываем функцию для получения нового текста и клавиатуры
        new_text, new_reply_markup = await func(callback, *args, **kwargs)

        if not new_reply_markup:
            new_reply_markup = InlineKeyboardMarkup(inline_keyboard=[])

        # Обновляем текст сообщения и клавиатуру
        await callback.message.edit_text(text=new_text, reply_markup=new_reply_markup)

        # Закрываем инлайн-уведомление
        await callback.answer()

    return wrapper


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def convert_to_moscow_time(utc_dt: datetime):
    # Установка часового пояса UTC для входного времени
    utc_zone = pytz.timezone("UTC")
    moscow_zone = pytz.timezone("Europe/Moscow")

    # Перевод времени из UTC в московское время
    utc_dt = utc_zone.localize(utc_dt)
    moscow_dt = utc_dt.astimezone(moscow_zone)

    # Форматирование даты в нужный формат
    return moscow_dt.strftime("%d.%m %H:%M")

