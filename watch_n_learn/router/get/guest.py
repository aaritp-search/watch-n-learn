from typing import Union

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter

from watch_n_learn.helper.template import TEMPLATE
from watch_n_learn.helper.template import flash
from watch_n_learn.helper.token import get_user

guest_get_router = APIRouter()

@guest_get_router.get("/")
async def index(request_: Request) -> HTMLResponse:

    user = await get_user(request_)

    if user is None:
        response = TEMPLATE.TemplateResponse("guest/index.jinja2", {"request": request_})
        response.delete_cookie("authentication_token")

        return response

    return TEMPLATE.TemplateResponse("user/index.jinja2", {"request": request_, "user": user})

@guest_get_router.get("/internal/logout")
async def logout(request_: Request) -> RedirectResponse:

    user = await get_user(request_)

    response = RedirectResponse("/", status.HTTP_302_FOUND)

    response.delete_cookie("authentication_token")

    if user is not None:
        flash(request_, "You have logged out")

    return response

@guest_get_router.get("/login")
async def login(request_: Request) -> Union[HTMLResponse, RedirectResponse]:

    user = await get_user(request_)

    if user is None:
        response = TEMPLATE.TemplateResponse("guest/login.jinja2", {"request": request_})
        response.delete_cookie("authentication_token")

        return response

    return RedirectResponse("/", status.HTTP_302_FOUND)

@guest_get_router.get("/sign-up")
async def sign_up(request_: Request) -> Union[HTMLResponse, RedirectResponse]:

    user = await get_user(request_)

    if user is None:
        response = TEMPLATE.TemplateResponse("guest/sign_up.jinja2", {"request": request_})
        response.delete_cookie("authentication_token")

        return response

    return RedirectResponse("/", status.HTTP_302_FOUND)
