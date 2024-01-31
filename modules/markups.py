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
        builder.row(InlineKeyboardButton(text='📝 Просмотреть описание сбора', callback_data='view_desc'))

    return builder.as_markup()

async def markup_fund_menu(number: int):
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text='✍️ Ввести данные о переводе', callback_data=f'{number}_enter_info'))
    builder.row(InlineKeyboardButton(text='❓ Как помочь?', callback_data=f'{number}_how_help'))

    return builder.as_markup()

async def markup_how_help_back(number: int):
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text='🔙 Назад', callback_data=f'{number}_back'))

    return builder.as_markup()

async def markup_confirm_enter_data():
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text='✅ Всё верно', callback_data='confirm_enter'))
    builder.row(InlineKeyboardButton(text='✍️ Ввести занова', callback_data='rewrite_enter'))
    builder.row(InlineKeyboardButton(text='❌ Отменить', callback_data='cancel_enter'))

    return builder.as_markup()