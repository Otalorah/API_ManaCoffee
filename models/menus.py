from pydantic import BaseModel

class ItemMenu(BaseModel):
    name: str
    price: int
    amount: str

class MessageMenuCreated(BaseModel):
    message: str
    num_items: int