from typing import List
from models.menus import ItemMenu
from typing import Dict, Tuple, Optional
from classes.google_sheet_menu import GoogleSheetMenu

sheet = GoogleSheetMenu()

# - - - - - - - - - - - - - - - - - - - - - Funciones Google Sheets - - - - - - - - - - - - - - - - - - - - -

def update_menu_sheet(items: List[ItemMenu]) -> int:
    num_items = len(items)
    sheet_data = [
        [item.name, item.price, item.amount] 
        for item in items
    ]
    sheet.write_menu(values=sheet_data, num_items=num_items)
   
    return num_items

def convert_to_dictionary(table: list[list]) -> list[dict]:

    menu = list()
    columns_name = ["name", "price", "amount"]

    for row in table:
        item_dict = dict(zip(columns_name, row))
        item_dict['price'] = int(item_dict['price'])
        menu.append(item_dict)

    return menu

def get_menu_sheet() -> List[ItemMenu]:
    table = sheet.get_menu()
    return convert_to_dictionary(table)