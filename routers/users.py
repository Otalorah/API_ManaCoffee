from fastapi import Depends, APIRouter, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from typing import Annotated

from models import models

from lib.utils import transform_to_bool
from lib.auth import create_token_user, aut_user, verify_token
from lib.functions_users import create_user_sheet, get_data_user, verify_password, update_password

router = APIRouter()

# - - - - - - - - - - - - - - - - - - - - - - - - - ENDPOINTS - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Create User in database


@router.post("/create", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_user(user: models.UserCreate) -> dict:

    name, email = create_user_sheet(user)

    token = create_token_user(email=email)

    return {"redirect": "/password", "access_token": token}

# Login the user with database



@router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
def login(data: models.EmailPasswordLogin) -> dict:

    def exception(str): return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=str)
    
    db_user = get_data_user(email=data.email)
    if not db_user:
        raise exception("El usuario no existe")
    
    if not verify_password(email=data.email, password=data.password):
        raise exception("La contraseña no es correcta")
    
    
    token = create_token_user(email=data.email)
    
    return {"redirect": "/inicio", "access_token": token}

# Get the User with a token


@router.get("/", response_model=models.UserBase, status_code=status.HTTP_200_OK)
def get_user(username: Annotated[None, Depends(aut_user)], token: HTTPAuthorizationCredentials = Depends(verify_token)) -> models.UserBase:
    return get_data_user(username=username)

# Get the value token with a token


@router.get("/token", response_model=dict, status_code=status.HTTP_200_OK)
def get_token(token: HTTPAuthorizationCredentials = Depends(verify_token)) -> dict[str]:
    return token

# Update the password


@router.put("/password", response_model=dict, status_code=status.HTTP_202_ACCEPTED)
def change_password(password: models.UserPassword, token: HTTPAuthorizationCredentials = Depends(verify_token)) -> dict:

    password = dict(password)["password"]
    print(token)

    update_password(email=token["email"], password=password)

    return {"message": "Cambio de contraseña exitoso"}
