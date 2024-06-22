import datetime
import os
from typing import AsyncGenerator, Optional

from fastapi import Depends
from fastapi_users.models import UP
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import Column, Integer, ForeignKey, Text, UUID, String, select, func, JSON, DateTime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

DATABASE_URL = os.getenv('DATABASE_URL')

Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    username = mapped_column(
            String(length=50), unique=True, index=True, nullable=False
        )
    email: Mapped[str] = mapped_column(
            String(length=320), unique=False, index=False, nullable=True
        )

    async def get_by_username(self, username: str) -> Optional[UP]:
        statement = select(self.user_table).where(
            func.lower(self.user_table.username) == func.lower(username)
        )
        return await self._get_user(statement)


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID, ForeignKey("user.id"))
    chat_id = Column(String, nullable=False, unique=True)
    model = Column(String, nullable=False)
    messages = Column(JSON, nullable=False)  # Хранение сообщений в формате JSON
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime,
                        default=datetime.datetime.now(datetime.timezone.utc),
                        onupdate=datetime.datetime.now(datetime.timezone.utc))

    user = relationship("User")


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
