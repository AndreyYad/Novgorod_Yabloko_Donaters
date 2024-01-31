from aiogram import types

from .bot_commands import send_msg, edit_msg_text
from .text import text
from .get_text import get_text_list_fundraiser
from .markups import markup_red_fundraisers

async def send_red_fund(chat_id: int):
    await send_msg(
        chat_id,
        text.red_fundraisers.format(await get_text_list_fundraiser()),
        markup=await markup_red_fundraisers()
    )
    
async def edit_enter_data(number: int, step: int, msg: types.Message):
    await edit_msg_text(
        text.enter_info_text(number, step),
        msg.chat.id,
        msg.message_id
    )
    await send_msg(
        msg.chat.id,
        text.enter_info_text(number, step)
    )