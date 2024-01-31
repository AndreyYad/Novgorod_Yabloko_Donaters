from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from re import fullmatch

from modules.text import text
from modules.bot_commands import send_msg, reply_msg
from modules.markups import markup_start, markup_fund_menu, markup_confirm_enter_data
from modules.get_text import get_text_list_fundraiser
from modules.states import FSMClient
from modules.database import get_fundraisers, get_fund_data
from modules.diagram import create_diagram

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
    elif await get_fundraisers() is None or int(msg.text) not in range(1, len(await get_fundraisers())+1):
        await send_msg(msg.chat.id, text.warning_fund_not_found)
    else:
        await state.clear()
        fund = await get_fund_data(int(msg.text))
        url = await create_diagram(fund[4], fund[3])
        await send_msg(
            msg.chat.id, 
            text.fund_info.format(fund[1], fund[2]).replace(' ', f'<a href="{url}"> </a>'), 
            markup=await markup_fund_menu(int(msg.text)),
            disable_web_page_preview=False
        )

async def get_enter_fio(msg: types.Message, state: FSMContext):
    if fullmatch(r'([А-ЯЁ][а-яё]+( |\Z)){3}', msg.text):
        await state.update_data(enter_fio=msg.text)
        await state.set_state(FSMClient.enter_phone)
        number = (await state.get_data())['number_enter']
        await send_msg(
            msg.chat.id,
            await text.enter_info_text(number, 2)
        )
    else:
        await reply_msg(msg, text.warning_no_template)

async def get_enter_phone(msg: types.Message, state: FSMContext):
    if fullmatch(r'\+7\d{10}\Z', msg.text):
        await state.update_data(enter_phone=msg.text)
        await state.set_state(FSMClient.enter_region)
        number = (await state.get_data())['number_enter']
        await send_msg(
            msg.chat.id,
            await text.enter_info_text(number, 3)
        )
    else:
        await reply_msg(msg, text.warning_no_template)

async def get_enter_region(msg: types.Message, state: FSMContext):
    if fullmatch(r'[А-ЯЁа-яё ]+\Z', msg.text): 
        await state.update_data(enter_region=msg.text)
        await state.set_state(FSMClient.enter_summ)   
        number = (await state.get_data())['number_enter']
        await send_msg(
            msg.chat.id,
            await text.enter_info_text(number, 4)
        )  
    else:
        await reply_msg(msg, text.warning_no_template)              

async def get_enter_summ(msg: types.Message, state: FSMContext):
    if fullmatch(r'\d+\Z', msg.text): 
        number = (await state.get_data())['number_enter']
        await state.update_data(enter_summ=int(msg.text))
        data = await state.get_data()
        await send_msg(
            msg.chat.id, 
            await text.get_confirm_data_text(number, data),
            markup=await markup_confirm_enter_data()
        )
        await state.set_state(FSMClient.confirm_enter_data)
    else:
        await reply_msg(msg, text.warning_no_template)

async def register_generic_handlers():
    router.message.register(start_func, CommandStart(), StateFilter(default_state))
    router.message.register(cancel_func, Command('cancel'), ~StateFilter(default_state))
    router.message.register(fundraisers_list_users_func, Command('fundraisers'), StateFilter(default_state))
    router.message.register(fundraiser_menu_func, F.text, StateFilter(FSMClient.open_fund))
    router.message.register(get_enter_fio, F.text, StateFilter(FSMClient.enter_fio))
    router.message.register(get_enter_phone, F.text, StateFilter(FSMClient.enter_phone))
    router.message.register(get_enter_region, F.text, StateFilter(FSMClient.enter_region))
    router.message.register(get_enter_summ, F.text, StateFilter(FSMClient.enter_summ))