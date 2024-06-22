import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Chat
from app.models.chat import ChatMessageIn


async def get_chat(chat_id: str, session: AsyncSession) -> Chat:
    result = await session.execute(select(Chat).where(Chat.chat_id == chat_id).limit(1))
    return result.scalars().first()


async def get_chats(user_id: uuid.UUID, session: AsyncSession) -> list[Chat]:
    result = await session.execute(select(Chat).where(Chat.user_id == user_id).order_by(Chat.updated_at.desc()))
    return list(result.scalars().all())


async def create_chat(user_id: uuid.UUID, chat_id: str, model: str, chat_messages: list[ChatMessageIn],
                      session: AsyncSession) -> Chat:
    new_chat = Chat(user_id=user_id, chat_id=chat_id, model=model, messages=chat_messages)
    session.add(new_chat)
    return new_chat


async def update_chat(chat_id: str, chat_message: ChatMessageIn, session: AsyncSession) -> Chat:
    chat = await get_chat(chat_id, session)
    chat.messages.append(chat_message)

    return chat
