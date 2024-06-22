import uuid
from datetime import datetime

from pydantic import BaseModel


class ChatMessageIn(BaseModel):
    role: str
    content: str


class ChatCreateIn(BaseModel):
    model: str
    message: ChatMessageIn


class ChatUpdateIn(BaseModel):
    chat_id: str
    model: str
    message: ChatMessageIn


class ChatMessageOut(BaseModel):
    role: str
    content: str


class ChatOut(BaseModel):
    chat_id: str
    user_id: uuid.UUID
    model: str
    messages: list[ChatMessageOut]
    created_at: datetime
    updated_at: datetime
