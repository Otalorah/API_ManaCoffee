import gspread
from os import getenv
from json import loads
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS = getenv('GOOGLE')
CREDENTIALS = loads(CREDENTIALS)
DOCUMENT = "ManaCoffe"
SHEET_NAME = "Menu"


class GoogleSheetMenu:
    def __init__(self):
        self.gc = gspread.service_account_from_dict(CREDENTIALS)
        self.sh = self.gc.open(DOCUMENT)
        self.sheet = self.sh.worksheet(SHEET_NAME)

    def get_range_data(self):
        last_row = len(self.sheet.col_values(1)) + 1
        return f'A2:B{last_row}'

    def write_menu(self, values: list[list], num_items: int) -> None:
        new_range = f'A2:B{num_items+1}'
        last_range = self.get_range_data()
        self.sheet.batch_clear([last_range])
        self.sheet.update(range_name=new_range, values=values)

    def get_menu(self):
        range = self.get_range_data()
        return self.sheet.get(range)