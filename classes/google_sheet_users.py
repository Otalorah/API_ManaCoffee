import gspread
from os import getenv
from json import loads
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS = getenv('GOOGLE')
CREDENTIALS = loads(CREDENTIALS)
DOCUMENT = "ManaCoffe"
SHEET_NAME = "Usuarios"


class GoogleSheetUsers:
    def __init__(self):
        self.gc = gspread.service_account_from_dict(CREDENTIALS)
        # self.gc = gspread.service_account(filename=file_name)
        self.sh = self.gc.open(DOCUMENT)
        self.sheet = self.sh.worksheet(SHEET_NAME)

    def write_data(self, range: str, values: list[list]) -> None:
        self.sheet.update(range_name=range, values=values)

    def get_data_by_email(self, email: str) -> bool | list:

        cell = self.sheet.find(email, in_column=3)

        if not cell:
            return False

        row = cell.row
        return self.sheet.row_values(row=row)[:5]

    def get_last_row_range(self) -> str:

        last_row = len(self.sheet.col_values(1)) + 1
        range_start = f"A{last_row}"
        range_end = f"D{last_row}"

        return f"{range_start}:{range_end}"

    def get_emails(self) -> list:
        return self.sheet.col_values(3)[1:]

    def get_code_email(self, email: str) -> list:

        cell = self.sheet.find(email)

        if not cell:
            return []

        cell_row = cell.row
      
        return self.sheet.row_values(row=cell_row)[4]

    def write_by_gmail(self, email: str, value: str, column: str) -> None:

        cell = self.sheet.find(email)
        row = cell.row

        self.sheet.update(range_name=f"{column}{row}", values=[[value]])

    def get_admin_emails(self) -> list:
        return self.sheet.col_values(8)[1:]
