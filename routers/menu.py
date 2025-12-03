from typing import List
from fastapi import APIRouter, status
from models.menus import ItemMenu, MessageMenuCreated
from classes.google_sheet_menu import GoogleSheetMenu
from lib.functions_menu import update_menu_sheet, get_menu_sheet

router = APIRouter()

# [
#  {"name": "Laptop", "price": 1500, "amount": "5"},
#  {"name": "Mouse", "price": 25, "amount": "10"}
# ]

@router.put("/update", response_model=MessageMenuCreated, status_code=status.HTTP_200_OK)
async def update_menu(items: List[ItemMenu]) -> MessageMenuCreated:

    num_items = update_menu_sheet(items)

    return {
        "message": "Menu created",
        "num_items": num_items
    }

@router.get("/get", response_model=List[ItemMenu], status_code=status.HTTP_200_OK)
async def get_menu() -> List[ItemMenu]:
    return get_menu_sheet()