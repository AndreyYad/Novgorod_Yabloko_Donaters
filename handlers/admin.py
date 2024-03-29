from aiogram import Router, types, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext

from modules.text import text
from modules.bot_commands import send_msg, send_msg_photo
from modules.states import FSMClient
from modules.database import save_fundraiser, get_fundraisers, delete_fundraiser, set_collected_money, get_fund_data
from modules.send_msg_template import send_red_fund

from modules.diagram import create_diagram

router = Router()

async def test(msg: types.Message):
    url = await create_diagram(2500, 9000)
    await send_msg(msg.chat.id, f'бла<a href="{url}"> </a>бла', disable_web_page_preview=False)

async def add_fund_handline_func(msg: types.Message, state: FSMContext):
    await state.update_data(add_fund_handline=msg.text)
    await state.set_state(FSMClient.add_fund_desc)
    await send_msg(msg.chat.id, text.add_fund_desc)

async def add_fund_desc_func(msg: types.Message, state: FSMContext):
    await state.update_data(add_fund_desс=msg.text)
    await state.set_state(FSMClient.add_fund_need_money)
    await send_msg(msg.chat.id, text.add_fund_need_money)

async def add_fund_need_money_func(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await send_msg(msg.chat.id, text.warning_not_number)
    else:
        await state.update_data(add_fund_need_money=int(msg.text))
        await save_fundraiser(await state.get_data())
        await state.clear()
        await send_msg(msg.chat.id, text.add_fund_succes)
        await send_red_fund(msg.chat.id)
        
async def delete_fund_func(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await send_msg(msg.chat.id, text.warning_not_number)
    elif int(msg.text) not in range(1, len(await get_fundraisers())+1):
        await send_msg(msg.chat.id, text.warning_fund_not_found)
    else:
        await state.clear()
        await delete_fundraiser(int(msg.text))
        await send_msg(msg.chat.id, text.delete_fund_succes)
        await send_red_fund(msg.chat.id)
        
async def set_money_num_func(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await send_msg(msg.chat.id, text.warning_not_number)
    elif int(msg.text) not in range(1, len(await get_fundraisers())+1):
        await send_msg(msg.chat.id, text.warning_fund_not_found)
    else:
        await state.update_data(set_money_num=int(msg.text))
        await state.set_state(FSMClient.set_money_value)
        await send_msg(msg.chat.id, text.set_money_value)
        
async def set_money_value_func(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await send_msg(msg.chat.id, text.warning_not_number)
    else:
        number = (await state.get_data())['set_money_num']
        await set_collected_money(number, int(msg.text))
        await state.clear()
        await send_msg(msg.chat.id, text.set_money_succes)
        await send_red_fund(msg.chat.id)
        
async def view_desc_num_func(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await send_msg(msg.chat.id, text.warning_not_number)
    elif int(msg.text) not in range(1, len(await get_fundraisers())+1):
        await send_msg(msg.chat.id, text.warning_fund_not_found)
    else:
        await state.clear()
        fund = await get_fund_data(int(msg.text))
        print(fund)
        await send_msg(msg.chat.id, text.view_desc_res.format(fund[1], fund[2]))

async def register_admin_handlers():
    router.message.register(add_fund_handline_func, F.text, StateFilter(FSMClient.add_fund_handline))
    router.message.register(add_fund_desc_func, F.text, StateFilter(FSMClient.add_fund_desc))
    router.message.register(add_fund_need_money_func, F.text, StateFilter(FSMClient.add_fund_need_money))
    router.message.register(delete_fund_func, F.text, StateFilter(FSMClient.delete_fund))
    router.message.register(set_money_num_func, F.text, StateFilter(FSMClient.set_money_num))
    router.message.register(set_money_value_func, F.text, StateFilter(FSMClient.set_money_value))
    router.message.register(view_desc_num_func, F.text, StateFilter(FSMClient.view_desc))
    
    router.message.register(test, Command('test'))