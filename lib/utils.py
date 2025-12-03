import random

from fastapi import HTTPException, status

def get_first_word(text: str) -> str:

    if not ' ' in text:
        return text.capitalize()

    for i, letter in enumerate(text):
        if letter == ' ':
            return text[:i].capitalize()

def transform_to_bool(text: str) -> bool:
    if text == 'TRUE':
        return True
    elif text == 'FALSE':
        return False

def generate_code():
    return str(random.randint(100000, 999999))

def exception(str): 
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=str
     )
