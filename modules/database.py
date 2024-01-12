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
        await cur.execute(
            "INSERT INTO fundraisers (handlers, description_text, need_to_raise, collected) VALUES (?, ?, ?, 0)", 
            (
                data['add_fund_handline'],
                data['add_fund_desc'],
                data['add_fund_need_money']
            )
        )
        await conn.commit()
        
async def get_index(number: int):
    return [fund[0] for fund in await get_fundraisers()][number-1]
        
async def delete_fundraiser(number: int):
    index_ = await get_index(number)
    async with connect('database/fundraisers.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("DELETE FROM fundraisers WHERE index_ = ?", (index_,))
        await conn.commit()
        
async def set_collected_money(number: int, value: int):
    index_ = await get_index(number)
    async with connect('database/fundraisers.sql') as conn:
        cur = await conn.cursor()
        await cur.execute("UPDATE fundraisers SET collected = ? WHERE index_ = ?", (value, index_))
        await conn.commit()