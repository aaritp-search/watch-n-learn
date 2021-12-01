from typing import Dict
from typing import List
from typing import Union
from urllib.parse import parse_qs

from fastapi.requests import Request

async def body_to_json(request__: Request, parameters_: List[str]) -> Union[Dict[str, str], str]:

    parsed_body = parse_qs((await request__.body()).decode("utf-8"), True)

    received_parameters = parsed_body.keys()

    for parameter in parameters_:
        if parameter not in received_parameters:

            return {}

    for parameter, value in parsed_body.items():
        if not value[-1]:

            return parameter

    return {parameter: value[-1] for parameter, value in parsed_body.items()}
