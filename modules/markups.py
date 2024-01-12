from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .config import ADMINS
from .database import get_fundraisers

async def markup_start(user_id: int):
    builder = InlineKeyboardBuilder()

    if user_id in ADMINS:
        builder.row(
            InlineKeyboardButton(text=':Работа со сборами:', callback_data='red_fundraisers')
        )

    return builder.as_markup()

async def markup_red_fundraisers():
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text='💸 Добавить сбор', callback_data='add_fundraiser'))
    if await get_fundraisers() is not None:
        builder.row(InlineKeyboardButton(text='🗑️ Удалить сбор', callback_data='delete_fundraiser'))
        builder.row(InlineKeyboardButton(text='✍️ Изменить собранную сумму', callback_data='set_money'))

    return builder.as_markup()