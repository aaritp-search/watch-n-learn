from fastapi import status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from watch_n_learn.authentication.main import get_user
from watch_n_learn.authentication.main import manager
from watch_n_learn.database.main import session
from watch_n_learn.database.models import User
from watch_n_learn.helper.parse import body_to_json
from watch_n_learn.helper.template import flash

guest_post_router = APIRouter(prefix="/internal")

@guest_post_router.post("/login")
async def login(request_: Request) -> RedirectResponse:

    data = body_to_json(await request_.body(), ["username", "password"])
    requests = 0
    while requests < 3:
        if data is None:
            flash(request_, "Invalid request")

            return RedirectResponse("/login", status.HTTP_302_FOUND)

        username = data["username"]

        user = get_user(username)

        if user is None:
            flash(request_, "Invalid username")

            return RedirectResponse("/login", status.HTTP_302_FOUND)

        if data["password"] != user.password:
            flash(request_, "Invalid password")

            return RedirectResponse("/login", status.HTTP_302_FOUND)

        flash(request_, "Logged in")

        response = RedirectResponse("/", status.HTTP_302_FOUND)

        response.set_cookie("authentication_token", manager.create_access_token(data={"sub": username}))

        return response

@guest_post_router.post("/sign-up")
async def sign_up(request_: Request) -> RedirectResponse:

    data = body_to_json(await request_.body(), ["username", "password"])

    if data is None:
        flash(request_, "Invalid request")

        return RedirectResponse("/sign-up", status.HTTP_302_FOUND)

    username_ = data["username"]

    if get_user(username_):
        flash(request_, "Username exists")

        return RedirectResponse("/sign-up", status.HTTP_302_FOUND)

    user = User(username=username_, password=data["password"])

    session.add(user)

    session.commit()

    session.expire(user)

    flash(request_, "Signed up")

    return RedirectResponse("/", status.HTTP_302_FOUND)
