'''
Модуль с командами для бота
'''

from loguru import logger
from aiogram import types, exceptions

from bot.bot import bot
from .config import TOKEN

empty_markups = types.InlineKeyboardMarkup(inline_keyboard=[[]])

async def send_msg(chat_id: int, text: str, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Отправка сообщения'''
    return await bot.send_message(chat_id, text, reply_markup=markup, **kwargs)

async def send_msg_photo(chat_id: int, photo: types.InputFile, text: str, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Отправка фото'''
    return await bot.send_photo(chat_id, photo, caption=text, reply_markup=markup, **kwargs)

async def reply_msg(msg: types.Message, text: str, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Ответ на сообщение'''
    return await msg.reply(text, reply_markup=markup, **kwargs)
    
async def edit_msg_text(text: str, chat_id: int, msg_id: int, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Редактирование сообщения'''
    try:
        await bot.edit_message_text(text, chat_id, msg_id, reply_markup=markup, **kwargs)
        return True
    except exceptions.TelegramBadRequest as error:
        logger.error(error)
        return False

async def edit_msg_caption(text: str, chat_id: int, msg_id: int, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Редактирование подписи(текста в сообщении с медиа)'''
    try:
        await bot.edit_message_caption(chat_id, msg_id, caption=text, reply_markup=markup, **kwargs)
        return True
    except exceptions.TelegramBadRequest as error:
        logger.error(error)
        return False
    
async def edit_msg_any(text: str, chat_id: int, msg_id: int, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Редактирвоание любого сообщения с текстом'''
    args = [text, chat_id, msg_id, markup]
    if not await edit_msg_caption(*args, **kwargs):
        await edit_msg_text(*args, **kwargs)
        
async def delete_msg(chat_id: int, msg_id: int):
    '''Удаление сообщения'''
    await bot.delete_message(chat_id, msg_id)
    
async def get_inputfile(file_id: str):
    '''Получение файла по его айди'''
    return types.input_file.URLInputFile(
        'https://api.telegram.org/file/bot{}/{}'.format(
            TOKEN, 
            (await bot.get_file(file_id)).file_path
        )
    )
    
# async def get_file_url()