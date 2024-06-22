import os
import uuid
from typing import Optional

import redis.asyncio
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    RedisStrategy, )
from fastapi_users.db import SQLAlchemyUserDatabase

from app.db.models import User, get_user_db

_SECRET = os.getenv("USER_SECRET_PHRASE")


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = _SECRET
    verification_token_secret = _SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)

_lifetime_seconds = 3600
_cookie_transport = CookieTransport(cookie_name="user_token", cookie_max_age=_lifetime_seconds)
_redis = redis.asyncio.Redis(host='redis', port=6379, decode_responses=True)


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(_redis, lifetime_seconds=_lifetime_seconds)


auth_backend = AuthenticationBackend(
    name="redis",
    transport=_cookie_transport,
    get_strategy=get_redis_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
