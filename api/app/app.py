import os

import openai
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.controllers.chat import create_chat_controllers
from app.controllers.user import create_user_controllers
from app.init_db import init_users
from app.services.user_manager import fastapi_users, auth_backend

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/api/auth", tags=["auth"]
)

openai.api_key = os.getenv('OPENAI_API_KEY')


@app.on_event("startup")
async def on_startup():
    print("Starting up...")
    await init_users()


create_user_controllers(app)
create_chat_controllers(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
