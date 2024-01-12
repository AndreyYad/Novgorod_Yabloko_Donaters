from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F, Router

from modules.bot_commands import edit_msg_text
from modules.text import text
from modules.states import FSMClient
from modules.send_msg_template import send_red_fund
from modules.get_text import get_text_list_fundraiser
from modules.database import get_fundraisers

router = Router()

async def callback_red_fundraisers(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await send_red_fund(call.message.chat.id)
    
async def callback_add_fundraisers(call: CallbackQuery, state: FSMContext):
    await state.set_state(FSMClient.add_fund_handline)
    await edit_msg_text(
        text.add_fund_handline,
        call.message.chat.id,
        call.message.message_id
    )
        
async def callback_delete_fundraisers(call: CallbackQuery, state: FSMContext):
    await state.set_state(FSMClient.delete_fund)
    if await get_fundraisers() is None:
        await call.answer('Сейчас нет никаких сборов!')
    else:
        await edit_msg_text(
            text.delete_fund.format(await get_text_list_fundraiser()),
            call.message.chat.id,
            call.message.message_id
        )
        
async def set_money_func(call: CallbackQuery, state: FSMContext):
    await state.set_state(FSMClient.set_money_num)
    if await get_fundraisers() is None:
        await call.answer('Сейчас нет никаких сборов!')
    else:
        await edit_msg_text(
            text.set_money.format(await get_text_list_fundraiser()),
            call.message.chat.id,
            call.message.message_id
        )
                
async def register_callbacks():
    router.callback_query.register(callback_red_fundraisers, F.data == 'red_fundraisers')
    router.callback_query.register(callback_add_fundraisers, F.data == 'add_fundraiser')
    router.callback_query.register(callback_delete_fundraisers, F.data == 'delete_fundraiser')
    router.callback_query.register(set_money_func, F.data == 'set_money')