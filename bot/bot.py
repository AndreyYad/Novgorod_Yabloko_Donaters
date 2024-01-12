from aiogram import Bot

from modules.config import TOKEN

bot = Bot(
    token=TOKEN,
    parse_mode='html',
    disable_web_page_preview=True
)