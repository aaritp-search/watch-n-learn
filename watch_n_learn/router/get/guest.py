from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

from watch_n_learn.helper.constant import TEMPLATE

guest_get_router = APIRouter()

@guest_get_router.get("/")
def index(request_: Request) -> HTMLResponse:

    return TEMPLATE.TemplateResponse("guest/index.jinja2", {"request": request_})
