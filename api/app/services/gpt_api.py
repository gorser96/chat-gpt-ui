import openai

from app.models.chat import ChatCreateIn


def create_chat_completion(data: ChatCreateIn):
    response = openai.chat.completions.create(
        model=data.chat.model,
        messages=[{'role': data.message.role, 'content': data.message.content}]
    )
    print(response)
    return response
