from asyncio import run
from os import system
from re import fullmatch

from modules.database import delete_donate, get_donates, get_fund_data

class DeleteDonate:

    menu = 'Exit - e\nReload donates - r\nDelete donate - del [index_donate:int] {minus_money:bool}\n'

    def __init__(self):
        while True:
            while True:
                system('cls')
                print(f'{run(self.get_list_donates())}{self.menu}')
                enter = input('Enter: ')
                if enter == 'r':
                    break
                elif enter == 'e':
                    quit()
                elif fullmatch(r'del \d+(\Z| (True|False))\Z', enter):
                    enter_list = enter.split(' ')
                    if len(enter_list) == 2:
                        enter_list.append('False')
                    run(delete_donate(int(enter_list[1]), enter_list[2]=='True'))

    @staticmethod
    async def get_list_donates():
        donates_data = await get_donates()
        text = ''
        list_names = ['index_', 'fundraiser_index', 'fio', 'phone', 'region', 'summ', 'user_tg_id', 'time']
        for donate_number, donate in enumerate(donates_data, 1):
            for index in range(8):
                add = ''
                if index == 1:
                    try:
                        add = f' ({(await get_fund_data(index_=donate[1]))[1]})'
                    except TypeError:
                        add = ' (None)'
                spaces = '-' * (17 - len(list_names[index]))
                text += f'{list_names[index]} {spaces} {donate[index]}{add}\n'
            text += '######################################\n'
        if not text:
            text = '##################\n### No donates ###\n##################\n\n'
        else:
            text = '####################################\n' + text + '\n'
        return text

if __name__ == '__main__':
    DeleteDonate()