from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import generic, callbacks, admin

storage = MemoryStorage()

dp = Dispatcher(storage=storage)

dp.include_routers(
    generic.router,
    callbacks.router,
    admin.router
)