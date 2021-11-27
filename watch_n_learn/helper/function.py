from typing import List

from fastapi.requests import Request

def flash(request__: Request, message_: str) -> None:

    if "_flashes" not in request__.session:
        request__.session["_flashes"] = []

    request__.session["_flashes"].append(message_)

def get_flashed_messages(request_: Request) -> List[str]:

    return request_.session.pop("_flashes") if "_flashes" in request_.session else []
