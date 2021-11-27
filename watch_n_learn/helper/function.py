from typing import Dict
from typing import List
from typing import Optional
from urllib.parse import parse_qs

from fastapi.requests import Request

def body_to_json(body_: str, fields_: List[str]) -> Optional[Dict]:

    parsed_json = parse_qs(body_)

    if list(parsed_json.keys()) != fields_:

        return None

    for value in parsed_json.values():
        if len(value) > 1:

            return None

    return {parameter: value[0] for parameter, value in parsed_json.items()}

def flash(request__: Request, message_: str) -> None:

    if "_flashes" not in request__.session:
        request__.session["_flashes"] = []

    request__.session["_flashes"].append(message_)

def get_flashed_messages(request_: Request) -> List[str]:

    return request_.session.pop("_flashes") if "_flashes" in request_.session else []
