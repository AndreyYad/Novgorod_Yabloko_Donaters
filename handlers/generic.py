from aiogram import Router, types
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from modules.text import text
from modules.bot_commands import send_msg, reply_msg
from modules.markups import markup_start

router = Router()

async def start_func(msg: types.Message):
    await send_msg(
        msg.chat.id, 
        text.start_text, 
        markup=await markup_start(msg.from_user.id)
    )
    
async def cancel_func(msg: types.Message, state: FSMContext):
    print(await state.get_state())
    await state.clear()
    await reply_msg(msg, 'Сброс')

async def register_generic_handlers():
    router.message.register(start_func, CommandStart(), StateFilter(default_state))
    router.message.register(cancel_func, Command('cancel'), ~StateFilter(default_state))