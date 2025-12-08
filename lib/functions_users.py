import hashlib
import bcrypt
from models import users
from fastapi import HTTPException, status
from typing import Dict, Tuple, Optional
from classes.google_sheet_users import GoogleSheetUsers

google = GoogleSheetUsers()

# - - - - - - - - - - - - - - - - - - - - - Funciones Google Sheets - - - - - - - - - - - - - - - - - - - - -

def verify_user_exists(email: str) -> None:
    emails_registered = google.get_emails()
    if email in emails_registered:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='El usuario ya existe'
        )

def hash_password(password: str) -> str:
    password_sha = hashlib.sha256(password.encode('utf-8')).digest()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_sha, salt).decode('utf-8')


def create_user_sheet(user: users.UserCreate) -> Tuple[str, str]:

    user_dict = user.model_dump()  
    email = user_dict['email']
    
    # Verificar si el usuario ya existe
    verify_user_exists(email)

    if not verify_admin_email(email):
       raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='El usuario no está registrado'
        )

    # Hashear la contraseña
    hashed_password = hash_password(user.password)
    user_dict['password'] = hashed_password
    
    # Preparar datos para Google Sheets
    user_values = [[valor for valor in user_dict.values()]]
    range_to_write = google.get_last_row_range()
    
    google.write_data(range=range_to_write, values=user_values)
    
    return user_dict['name'], user_dict['email']


def get_data_user(email: str) -> Optional[Dict[str, str]]:

    list_data = google.get_data_by_email(email=email)
    
    if not list_data:
        return None
    
    list_fields = [
        'name', 'lastname',
        'email', 'password'
    ]
    
    return dict(zip(list_fields, list_data))


def verify_password(email: str, password: str) -> bool:

    user_data = get_data_user(email=email)
    
    if not user_data:
        return False
    
    password_in_sheet = user_data['password']
    password_sha = hashlib.sha256(password.encode('utf-8')).digest()
    
    try:
        return bcrypt.checkpw(password_sha, password_in_sheet.encode('utf-8'))
    except Exception:
        return False


def update_password(email: str, password: str) -> None:

    hashed_password = hash_password(password)
    google.write_by_gmail(email=email, value=hashed_password, column="D")


def verify_email_registered(email: str) -> None:

    if email not in google.get_emails():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='El correo no se encuentra registrado'
        )


def verify_code(email: str, code: str) -> None:

    stored_code = google.get_code_email(email)
    
    if code != stored_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Código inválido'
        )


def write_code_gmail(email: str, code: str) -> None:
    google.write_by_gmail(email=email, value=code, column="E")


def verify_admin_email(email:str) -> bool:
    admin_emails = google.get_admin_emails()
    return email in admin_emails