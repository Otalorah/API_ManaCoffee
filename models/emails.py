from pydantic import BaseModel

class EmailPasswordLogin(BaseModel):
    email: str
    password: str
