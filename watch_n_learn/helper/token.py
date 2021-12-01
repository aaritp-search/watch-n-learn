from typing import Optional

from fastapi.exceptions import HTTPException
from fastapi.requests import Request

from watch_n_learn.authentication.main import manager
from watch_n_learn.database.models import User

async def get_user(request__: Request) -> Optional[User]:

    authentication_token = request__.cookies.get("authentication_token")

    try:

        return await manager.get_current_user(authentication_token)

    except HTTPException:
        pass

    return None
