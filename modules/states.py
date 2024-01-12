from aiogram.fsm.state import StatesGroup, State

class FSMClient(StatesGroup):
    
    add_fund_handline = State()
    add_fund_desc = State()
    add_fund_need_money = State()
    
    delete_fund = State()
    
    set_money_num = State()
    set_money_value = State()