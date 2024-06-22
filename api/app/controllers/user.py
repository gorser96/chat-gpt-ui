from fastapi import Depends, FastAPI

from app.db.models import User
from app.services.user_manager import current_active_user


def create_user_controllers(app: FastAPI):
    @app.get("/api/current-user")
    async def current_user(user: User = Depends(current_active_user)):
        return {'id': user.id, 'username': user.username}
