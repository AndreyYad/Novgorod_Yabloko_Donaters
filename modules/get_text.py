from .database import get_fundraisers

async def get_text_list_fundraiser(money: bool=True):
    list_fundraiser = await get_fundraisers()
    
    if list_fundraiser is None:
        result = 'Сборов нет!'
    else:
        result = ''.join([f'{i+1}. {list_fundraiser[i][1]}\n' + money * f' ({await get_beauty_num(list_fundraiser[i][4])} ₽ / {await get_beauty_num(list_fundraiser[i][3])} ₽)\n' for i in range(len(list_fundraiser))])
    
    return result

async def get_beauty_num(number: int|str):
    number = int(number)
    return '{:,}'.format(number).replace(',', '\'')