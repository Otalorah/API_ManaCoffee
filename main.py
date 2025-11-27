# http://127.0.0.1:8000
# uvicorn main:app --reload

from fastapi import FastAPI
from routers import users, email
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/user", tags=["user"])
app.include_router(email.router, prefix="/email", tags=["email"])


@app.get("/")
async def root():
    return {"message": "Hello ManaCoffe"}
