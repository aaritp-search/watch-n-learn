from fastapi import status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

from watch_n_learn.helper.constant import TEMPLATE

error_router = APIRouter()

@error_router.get("/{_:path}")
def not_found(request_: Request) -> HTMLResponse:

    return TEMPLATE.TemplateResponse(
        "error/404.jinja2", {"request": request_}, status.HTTP_404_NOT_FOUND
    )
