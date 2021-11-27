from fastapi import status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from watch_n_learn.database.main import session
from watch_n_learn.database.models import User
from watch_n_learn.helper.function import body_to_json
from watch_n_learn.helper.function import flash

guest_post_router = APIRouter(prefix="/internal")

@guest_post_router.post("/sign-up")
async def sign_up(request_: Request) -> RedirectResponse:

    body = body_to_json((await request_.body()).decode("utf-8"), ["username", "password"])

    if body is None:
        flash(request_, "Invalid request")

        return RedirectResponse("/sign-up", status.HTTP_302_FOUND)

    username_ = body["username"]

    if session.query(session.query(User).filter(User.username == username_).exists()).scalar():
        flash(request_, "Username exists")

        return RedirectResponse("/sign-up", status.HTTP_302_FOUND)

    user = User(username=username_, password=body["password"])
    session.add(user)
    session.commit()

    session.refresh(user)

    flash(request_, "You have signed up")

    return RedirectResponse("/", status.HTTP_302_FOUND)
