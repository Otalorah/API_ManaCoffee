import gspread
from os import getenv
from json import loads
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS = getenv('GOOGLE')
CREDENTIALS = loads(CREDENTIALS)
DOCUMENT = "ManaCoffe"
SHEET_NAME = "Reservas"


class GoogleSheetReservation:
    def __init__(self):
        self.gc = gspread.service_account_from_dict(CREDENTIALS)
        self.sh = self.gc.open(DOCUMENT)
        self.sheet = self.sh.worksheet(SHEET_NAME)

    def write_reservation(self, values: list) -> None:
        self.sheet.append_row(values)

    def get_reservations(self):
        last_row = len(self.sheet.col_values(1)) + 1
        range = f'A2:H{last_row}'
        return self.sheet.get(range)

    def update_reservations(self, values: list[list], num_items: int) -> None:
        new_range = f'A2:H{num_items+1}'

        last_row = len(self.sheet.col_values(1)) + 1
        last_range = f'A2:H{last_row}'

        self.sheet.batch_clear([last_range])
        self.sheet.update(range_name=new_range, values=values)