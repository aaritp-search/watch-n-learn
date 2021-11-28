from typing import Union

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from watch_n_learn.database.models import User
from watch_n_learn.helper.template import TEMPLATE
from watch_n_learn.helper.template import flash
from watch_n_learn.helper.token import get_authentication

guest_get_router = APIRouter()

@guest_get_router.get("/")
async def index(request_: Request) -> HTMLResponse:

    authentication = await get_authentication(request_)

    if isinstance(authentication, User):

        return TEMPLATE.TemplateResponse(
            "user/index.jinja2", {"request": request_, "user": authentication}
        )

    response = TEMPLATE.TemplateResponse("guest/index.jinja2", {"request": request_})

    if authentication:
        response.delete_cookie("authentication_token")

    return response

@guest_get_router.get("/internal/logout")
async def logout(request_: Request) -> RedirectResponse:

    authentication = await get_authentication(request_)

    response = RedirectResponse("/", status.HTTP_302_FOUND)

    if authentication is not False:
        response.delete_cookie("authentication_token")
        flash(request_, "Logged out")

    return response

@guest_get_router.get("/login")
async def login(request_: Request) -> Union[HTMLResponse, RedirectResponse]:

    authentication = await get_authentication(request_)

    if isinstance(authentication, User):
        flash(request_, "You are logged in")

        return RedirectResponse("/", status.HTTP_302_FOUND)

    response = TEMPLATE.TemplateResponse("guest/login.jinja2", {"request": request_})

    if authentication:
        response.delete_cookie("authentication_token")

    return response

@guest_get_router.get("/sign-up")
async def sign_up(request_: Request) -> Union[HTMLResponse, RedirectResponse]:

    authentication = await get_authentication(request_)

    if isinstance(authentication, User):
        flash(request_, "You are logged in")

        return RedirectResponse("/", status.HTTP_302_FOUND)

    response = TEMPLATE.TemplateResponse("guest/sign_up.jinja2", {"request": request_})

    if authentication:
        response.delete_cookie("authentication_token")

    return response
