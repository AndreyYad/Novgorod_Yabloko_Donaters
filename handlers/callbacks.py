from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F, Router
# from aiogram.utils.callback_answer import CallbackAnswer

from modules.bot_commands import edit_msg_text, delete_msg, send_msg
from modules.text import text
from modules.states import FSMClient
from modules.send_msg_template import send_red_fund
from modules.get_text import get_text_list_fundraiser
from modules.database import get_fundraisers, get_fund_data, save_donate
from modules.markups import markup_how_help_back, markup_fund_menu, markup_enter_data_succes

router = Router()

async def callback_red_fundraisers(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await send_red_fund(call.message.chat.id)
    # await call_answer.answered()
    
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
        
async def view_desc_func(call: CallbackQuery, state: FSMContext):
    await state.set_state(FSMClient.view_desc)
    if await get_fundraisers() is None:
        await call.answer('Сейчас нет никаких сборов!')
    else:
        await edit_msg_text(
            text.view_desc_num.format(await get_text_list_fundraiser()),
            call.message.chat.id,
            call.message.message_id
        )
        
async def how_help_func(call: CallbackQuery):
    number = int(call.data[:call.data.index('_')])
    await delete_msg(
        call.message.chat.id,
        call.message.message_id
    )
    await send_msg(
        call.message.chat.id, 
        text.how_help, 
        markup=await markup_how_help_back(number)
    )
    
async def how_help_back_func(call: CallbackQuery):
    number = int(call.data[:call.data.index('_')])
    fund = await get_fund_data(number)
    await delete_msg(
        call.message.chat.id,
        call.message.message_id
    )
    await send_msg(
        call.message.chat.id, 
        text.fund_info.format(fund[1], fund[2]),
        markup=await markup_fund_menu(number)
    )
    
async def start_enter_data(call: CallbackQuery, state: FSMContext):
    number = int(call.data[:call.data.index('_')])
    await state.set_state(FSMClient.enter_fio)
    await state.update_data(number_enter=number)
    await delete_msg(
        call.message.chat.id,
        call.message.message_id
    )
    await send_msg(
        call.message.chat.id,
        await text.enter_info_text(number, 1)
    )
    
async def rewrite_enter_data(call: CallbackQuery, state: FSMContext):
    number = (await state.get_data())['number_enter']
    await state.set_state(FSMClient.enter_fio)
    await edit_msg_text(
        await text.enter_info_text(number, 1),
        call.message.chat.id,
        call.message.message_id
    )
    
async def cancel_enter_data(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await edit_msg_text(
        text.cancel_enter_data,
        call.message.chat.id,
        call.message.message_id
    )
    
async def confirm_enter_data(call: CallbackQuery, state: FSMContext):
    number = (await state.get_data())['number_enter']
    await save_donate(number, await state.get_data(), call.from_user.id)
    await state.clear()
    await edit_msg_text(
        text.succes_enter_data,
        call.message.chat.id,
        call.message.message_id,
        markup=await markup_enter_data_succes()
    )

async def how_help_2_func(call: CallbackQuery):
    await edit_msg_text(
        text.how_help + '\n\nВернуться к списку сборов - /fundraisers',
        call.message.chat.id,
        call.message.message_id
    )
                
async def register_callbacks():
    router.callback_query.register(callback_red_fundraisers, F.data == 'red_fundraisers')
    router.callback_query.register(callback_add_fundraisers, F.data == 'add_fundraiser')
    router.callback_query.register(callback_delete_fundraisers, F.data == 'delete_fundraiser')
    router.callback_query.register(set_money_func, F.data == 'set_money')
    router.callback_query.register(view_desc_func, F.data == 'view_desc')
    router.callback_query.register(how_help_func, F.data.regexp(r'\d+_how_help'))
    router.callback_query.register(how_help_back_func, F.data.regexp(r'\d+_back'))
    router.callback_query.register(start_enter_data, F.data.regexp(r'\d+_enter_info'))
    router.callback_query.register(rewrite_enter_data, F.data == 'rewrite_enter')
    router.callback_query.register(cancel_enter_data, F.data == 'cancel_enter')
    router.callback_query.register(confirm_enter_data, F.data == 'confirm_enter')
    router.callback_query.register(how_help_2_func, F.data == 'how_help_2')
