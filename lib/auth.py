from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

from pydantic import BaseModel

from jose import jwt, JWTError

from os import getenv
from dotenv import load_dotenv

from datetime import datetime, timedelta, UTC

load_dotenv()

SECRET = getenv("SECRET")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_DAYS_DURATION = 1

security = HTTPBearer()

class Token(BaseModel):
    token: str
    token_type: str = 'bearer'


def create_token_user(email: str) -> Token:

    expire = datetime.now(UTC) + timedelta(days=ACCESS_TOKEN_DAYS_DURATION)
    content = {"email": email, "exp": expire}
    token = jwt.encode(content, SECRET, algorithm=ALGORITHM)

    return Token(token=token)


def create_token_code(email: str) -> Token:

    expire = datetime.now(UTC) + timedelta(hours=1)
    content = {"email": email, "exp": expire}
    token = jwt.encode(content, SECRET, algorithm=ALGORITHM)

    return Token(token=token)


async def aut_user(credentials: str = Depends(security)) -> str:

    token = credentials.credentials

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="No autorizado",
                              headers={"WWW-Aunthenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
    except JWTError:
        raise exception

    if username is None:
        raise exception

    return username


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Verifica que el token sea válido y retorna el payload completo
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
