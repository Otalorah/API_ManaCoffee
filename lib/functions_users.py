from fastapi import HTTPException, status
import hashlib
import bcrypt
from typing import Dict, Tuple, Optional
from models import models
from lib.utils import get_first_word
from classes.google_sheet_users import GoogleSheet_users

google = GoogleSheet_users()

# - - - - - - - - - - - - - - - - - - - - - Funciones Google Sheets - - - - - - - - - - - - - - - - - - - - -

def verify_user_exists(email: str) -> None:
    """
    Verifica si un usuario ya está registrado.
    
    Args:
        email: Correo electrónico del usuario
        
    Raises:
        HTTPException: Si el usuario ya existe
    """
    emails_registered = google.get_emails()
    if email in emails_registered:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='El usuario ya existe'
        )


def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando SHA256 + bcrypt.
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        str: Contraseña hasheada
    """
    password_sha = hashlib.sha256(password.encode('utf-8')).digest()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_sha, salt).decode('utf-8')


def create_user_sheet(user: models.UserCreate) -> Tuple[str, str]:
    """
    Crea un nuevo usuario en Google Sheets.
    
    Args:
        user: Datos del usuario a crear
        
    Returns:
        Tuple[str, str]: Nombre y email del usuario creado
        
    Raises:
        HTTPException: Si el usuario ya existe
    """
    user_dict = user.model_dump()  # Reemplaza dict(user) - más moderno
    email = user_dict['email']
    
    # Verificar si el usuario ya existe
    verify_user_exists(email)
    
    # Hashear la contraseña
    hashed_password = hash_password(user.password)
    user_dict['password'] = hashed_password
    
    # Preparar datos para Google Sheets
    user_values = [[valor for valor in user_dict.values()]]
    range_to_write = google.get_last_row_range()
    
    google.write_data(range=range_to_write, values=user_values)
    
    return user_dict['name'], user_dict['email']


def get_data_user(email: str) -> Optional[Dict[str, str]]:
    """
    Obtiene los datos de un usuario por username.
    
    Args:
        username: Nombre de usuario
        
    Returns:
        Optional[Dict[str, str]]: Diccionario con los datos del usuario o None
    """
    list_data = google.get_data_by_email(email=email)
    
    if not list_data:
        return None
    
    list_fields = [
        'name', 'lastname',
        'email', 'password'
    ]
    
    return dict(zip(list_fields, list_data))


def verify_password(email: str, password: str) -> bool:
    """
    Verifica si la contraseña es correcta para un usuario.
    
    Args:
        username: Nombre de usuario
        password: Contraseña en texto plano
        
    Returns:
        bool: True si la contraseña es correcta, False en caso contrario
    """
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
    """
    Actualiza la contraseña de un usuario.
    
    Args:
        email: Correo electrónico del usuario
        password: Nueva contraseña en texto plano
    """
    hashed_password = hash_password(password)
    google.write_by_gmail(email=email, value=hashed_password, column="D")


def verify_email_registered(email: str) -> None:
    """
    Verifica que un correo esté registrado en el sistema.
    
    Args:
        email: Correo electrónico a verificar
        
    Raises:
        HTTPException: Si el correo no está registrado
    """
    if email not in google.get_emails():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='El correo no se encuentra registrado'
        )


def verify_code(email: str, code: str) -> None:
    """
    Verifica que el código de verificación sea correcto.
    
    Args:
        email: Correo electrónico del usuario
        code: Código de verificación
        
    Raises:
        HTTPException: Si el código es inválido
    """
    stored_code = google.get_code_email(email)
    
    if code != stored_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Código inválido'
        )


def write_code_gmail(email: str, code: str) -> None:
    """
    Guarda el código de verificación para un email.
    
    Args:
        email: Correo electrónico del usuario
        code: Código de verificación a guardar
    """
    google.write_by_gmail(email=email, value=code, column="E")