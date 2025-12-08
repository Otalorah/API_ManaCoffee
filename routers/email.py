from fastapi import APIRouter, status

from models import users

from lib.utils import generate_code
from lib.functions_smtp import send_email_code
from lib.auth import create_token_code, Token
from lib.functions_users import verify_email_registered, verify_code, write_code_gmail

router = APIRouter()

# - - - - - - - - - - - - - - - - - - - - - - - - - ENDPOINTS - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Verify email user


@router.post("/", response_model=dict, status_code=status.HTTP_200_OK)
async def send_emails(email: users.EmailUser) -> dict:

    email = dict(email)["email"]

    verify_email_registered(email)

    code = generate_code()

    send_email_code(email=email, code=code)
    write_code_gmail(email=email, code=code)

    return {"message": "Correo enviado correctamente"}


# Verify code user


@router.post("/code", response_model=Token, status_code=status.HTTP_200_OK)
async def verify_codes(user: users.CodeUser) -> Token:

    user = dict(user)
    verify_code(email=user["email"], code=user["code"])

    return create_token_code(email=user["email"])
