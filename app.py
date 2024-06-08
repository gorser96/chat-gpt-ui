import os

import aiohttp
import openai
from fastapi import FastAPI, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from init_db import init_db
from models import User, Chat, SessionLocal

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

templates = Jinja2Templates(directory="templates")

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    request.session['username'] = username
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@app.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    request.session.pop('username', None)
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)


async def get_current_user(request: Request, db: Session = Depends(get_db)):
    username = request.session.get('username')
    if not username:
        return None
    return db.query(User).filter(User.username == username).first()


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("index.html", {"request": request, "username": user.username})


@app.post("/ask", response_class=HTMLResponse)
async def ask_question(request: Request, question: str = Form(...), db: Session = Depends(get_db)):
    user = await get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    async with aiohttp.ClientSession() as session:
        async with session.post(
                "https://api.openai.com/v1/completions",
                headers={
                    "Authorization": f"Bearer {openai.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-3.5-turbo-16k",
                    "prompt": question,
                    "max_tokens": 150,
                },
        ) as resp:
            response = await resp.json()
            answer = response['choices'][0]['text'].strip()
    chat = Chat(user_id=user.id, question=question, answer=answer)
    db.add(chat)
    db.commit()
    return templates.TemplateResponse("index.html", {"request": request, "question": question, "answer": answer,
                                                     "username": user.username})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
