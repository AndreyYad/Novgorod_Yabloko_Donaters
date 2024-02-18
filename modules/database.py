from aiosqlite import connect
from os import mkdir

async def create_database():
    try:
        mkdir('database')
    except FileExistsError:
        pass
    async with connect('database/fundraisers.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("CREATE TABLE IF NOT EXISTS fundraisers (index_ INTEGER PRIMARY KEY AUTOINCREMENT , handlers text, description_text text, need_to_raise int, collected int)")
        await cur.execute("CREATE TABLE IF NOT EXISTS donations (index_ INTEGER PRIMARY KEY AUTOINCREMENT, fundraiser_index int, fio text, phone text, region text, summ int, user_tg_id int, time datetime)")
        await conn.commit()
        
async def get_fundraisers():
    async with connect('database/fundraisers.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT * FROM fundraisers")
        result = await cur.fetchall()
        if len(result) == 0:
            result = None
        return result
    
async def save_fundraiser(data: dict[str, any]):
    async with connect('database/fundraisers.sql') as conn:
        cur = await conn.cursor()
        print(data)
        await cur.execute(
            "INSERT INTO fundraisers (handlers, description_text, need_to_raise, collected) VALUES (?, ?, ?, 0)", 
            (
                data['add_fund_handline'],
                data['add_fund_desс'],
                data['add_fund_need_money']
            )
        )
        await conn.commit()
        
async def get_index(number: int):
    print(number)
    return [fund[0] for fund in await get_fundraisers()][number-1]
        
async def delete_fundraiser(number: int):
    index_ = await get_index(number)
    async with connect('database/fundraisers.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("DELETE FROM fundraisers WHERE index_ = ?", (index_,))
        await cur.execute("DELETE FROM donations WHERE fundraiser_index = ?", (index_,))
        await conn.commit()
        
async def set_collected_money(number: int, value: int):
    index_ = await get_index(number)
    async with connect('database/fundraisers.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("UPDATE fundraisers SET collected = ? WHERE index_ = ?", (value, index_))
        await conn.commit()
        
async def get_fund_data(number: int=None, index_: int=None):
    if index_ is None:
        index_ = await get_index(number)
    print(number, index_)
    async with connect('database/fundraisers.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("SELECT * FROM fundraisers WHERE index_ = ?", (index_,))
        result = await cur.fetchall()
        return result[0]
    
async def save_donate(fundriser_index: str, data: dict, user_id: int):
    async with connect('database/fundraisers.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("INSERT INTO donations (fundraiser_index, fio, phone, region, summ, user_tg_id, time) VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)", 
            (
                fundriser_index,
                data['enter_fio'],
                data['enter_phone'],
                data['enter_region'],
                data['enter_summ'],
                user_id
            )
        )
        await cur.execute("UPDATE fundraisers SET collected = collected + ? WHERE index_ = ?", (data['enter_summ'], fundriser_index))
        await conn.commit()