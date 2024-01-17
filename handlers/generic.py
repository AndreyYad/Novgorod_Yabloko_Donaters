from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from modules.text import text
from modules.bot_commands import send_msg, reply_msg
from modules.markups import markup_start
from modules.get_text import get_text_list_fundraiser
from modules.states import FSMClient
from modules.database import get_fundraisers, get_fund_data

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
    
async def fundraisers_list_users_func(msg: types.Message, state: FSMContext):
    await send_msg(msg.chat.id, text.list_funds.format(await get_text_list_fundraiser(money=False)))
    await state.set_state(FSMClient.open_fund)
    
async def fundraiser_menu_func(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await send_msg(msg.chat.id, text.warning_not_number)
    elif int(msg.text) not in range(1, len(await get_fundraisers())+1):
        await send_msg(msg.chat.id, text.warning_fund_not_found)
    else:
        await state.clear()
        fund = await get_fund_data(int(msg.text))
        await send_msg(msg.chat.id, text.fund_info.format(fund[1], fund[2]))

async def register_generic_handlers():
    router.message.register(start_func, CommandStart(), StateFilter(default_state))
    router.message.register(cancel_func, Command('cancel'), ~StateFilter(default_state))
    router.message.register(fundraisers_list_users_func, Command('fundraisers'), StateFilter(default_state))
    router.message.register(fundraiser_menu_func, F.text, StateFilter(FSMClient.open_fund))