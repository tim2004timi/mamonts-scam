from aiogram import Dispatcher, Router, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
)

from .keyboards import menu_inline_keyboard, menu_reply_keyboard
from .utils import (
    edit_message,
)
from ..users.exceptions import UserExistsError

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    pass


@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    await menu(event=message)


@router.callback_query(F.data == "menu")
@edit_message
async def menu_callback(
    callback: CallbackQuery, state: FSMContext
) -> tuple[str, InlineKeyboardMarkup]:
    await state.clear()
    return await menu(event=callback)


@router.message(F.text == "📋 Меню")
async def menu_message(message: Message, state: FSMContext):
    await state.clear()
    await menu(event=message)


async def menu(event) -> None | tuple[str, InlineKeyboardMarkup]:
    pass


def get_permission_emoji(permission: bool):
    return "▫️" if permission else "▪️"


def register_handlers(dp: Dispatcher):
    dp.include_router(router)
