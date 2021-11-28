from contextvars import ContextVar
from typing import List

from blinker.base import Namespace
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

FLASHED_MESSAGE = Namespace().signal("flashed_message")

TEMPLATE = Jinja2Templates("watch_n_learn/template")

request_context = ContextVar("request_context")

def flash(request__: Request, message_: str) -> None:

    flashes = request__.session.get("_flashes", [])

    flashes.append(message_)

    request__.session["_flashes"] = flashes

    FLASHED_MESSAGE.send(id(flash), message=message_)

def get_flashed_messages(request_: Request) -> List[int]:

    flashes = request_context.get(None)

    if flashes is None:
        flashes = request_.session.pop("_flashes") if "_flashes" in request_.session else []
        request_context.set(flashes)

    return flashes

TEMPLATE.env.globals["get_flashed_messages"] = get_flashed_messages
