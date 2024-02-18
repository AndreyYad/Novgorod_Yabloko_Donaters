from asyncio import run
from vk_api.bot_longpoll import VkBotLongPoll

from bot.dispatcher import dp
from bot.bot import bot
from modules.register_handlers import register_handlers
from modules.database import create_database
from vk_bot.vk_bot import vk_session

from modules.diagram import create_diagram

async def main():
    await create_database()
    await register_handlers()
    print('Бот запущен!')
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        run(main())
    except KeyboardInterrupt:
        pass