from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User, get_async_session
from app.models.chat import ChatOut, ChatCreateIn, ChatMessageIn, ChatUpdateIn
from app.services.chat_service import get_chat, get_chats, create_chat, update_chat
from app.services.gpt_api import create_chat_completion
from app.services.user_manager import current_active_user


def create_chat_controllers(app: FastAPI):
    @app.get("/api/chats/{chat_id}", response_model=ChatOut)
    async def get(chat_id: str, user: User = Depends(current_active_user),
                  session: AsyncSession = Depends(get_async_session)) -> ChatOut:
        chat = await get_chat(chat_id, session)

        return ChatOut(chat_id=chat.chat_id, user_id=user.id, model=chat.model, messages=chat.messages,
                       created_at=chat.created_at, updated_at=chat.updated_at)

    @app.get("/api/chats", response_model=list[ChatOut])
    async def get_list(user: User = Depends(current_active_user),
                       session: AsyncSession = Depends(get_async_session)) -> list[ChatOut]:
        chats = await get_chats(user.id, session)

        return [ChatOut(chat_id=chat.chat_id, user_id=user.id, model=chat.model, messages=chat.messages,
                        created_at=chat.created_at, updated_at=chat.updated_at)
                for chat in chats]

    @app.put("/api/chats", response_model=ChatOut)
    async def create(data: ChatCreateIn,
                     user: User = Depends(current_active_user),
                     session: AsyncSession = Depends(get_async_session)) -> ChatOut:
        response = create_chat_completion(data)

        response_model = ChatMessageIn(role='assistant', content=response.choices[0].message.content)
        messages = [data.message, response_model]

        chat = await create_chat(user.id, response.id, data.model, messages, session)

        await session.commit()

        return ChatOut(chat_id=chat.chat_id, user_id=user.id, model=chat.model, messages=chat.messages,
                       created_at=chat.created_at, updated_at=chat.updated_at)

    @app.put("/api/chats/{chat_id}", response_model=ChatOut)
    async def update(data: ChatUpdateIn,
                     user: User = Depends(current_active_user),
                     session: AsyncSession = Depends(get_async_session)) -> ChatOut:
        chat = await update_chat(data.chat_id, data.message, session)

        response = create_chat_completion(chat.messages)

        response_model = ChatMessageIn(role='assistant', content=response.choices[0].message.content)

        chat = await update_chat(data.chat_id, response_model, session)

        await session.commit()

        return ChatOut(chat_id=chat.chat_id, user_id=user.id, model=chat.model, messages=chat.messages,
                       created_at=chat.created_at, updated_at=chat.updated_at)
