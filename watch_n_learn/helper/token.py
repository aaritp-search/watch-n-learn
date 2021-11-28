from typing import Union

from fastapi.exceptions import HTTPException
from fastapi.requests import Request

from watch_n_learn.authentication.main import manager
from watch_n_learn.database.models import User

async def get_authentication(request__: Request) -> Union[User, bool]:

    authentication_token = request__.cookies.get("authentication_token")

    if authentication_token is None:

        return False

    try:

        return await manager.get_current_user(authentication_token)

    except HTTPException:

        return True
