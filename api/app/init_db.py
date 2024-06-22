import os

from fastapi_users.exceptions import UserAlreadyExists
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.db.models import User, async_session_maker
from app.db.schemas import UserCreate
from app.services.user_manager import UserManager


async def init_users():
    async with async_session_maker() as session:
        # Получение пользователей из переменных окружения
        print('Try found users...')
        default_users = os.getenv("DEFAULT_USERS")
        if default_users:
            user_db = SQLAlchemyUserDatabase(session, User)
            user_manager = UserManager(user_db)
            print(f'Users found in env!')
            users = [user.split(":") for user in default_users.split(",")]
            for username, password in users:
                db_user = UserCreate(
                    username=username,
                    password=password,
                    email=f'{username}@test.com',
                    is_active=True)
                try:
                    await user_manager.create(db_user)
                    print(f'user {username} created')
                except UserAlreadyExists:
                    print(f'user {username} already exists')
