from .bot_commands import send_msg
from .text import text
from .get_text import get_text_list_fundraiser
from .markups import markup_red_fundraisers

async def send_red_fund(chat_id: int):
    await send_msg(
        chat_id,
        text.red_fundraisers.format(await get_text_list_fundraiser()),
        markup=await markup_red_fundraisers()
    )