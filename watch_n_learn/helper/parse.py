from typing import Dict
from typing import List
from typing import Optional
from urllib.parse import parse_qs

def body_to_json(body_: bytes, parameter_list_: List[str]) -> Optional[Dict]:

    parsed_body = parse_qs(body_.decode("utf-8"))

    if list(parsed_body.keys()) != parameter_list_:

        return None

    for value in parsed_body.values():
        if len(value) != 1:

            return None

    return {parameter: value[0] for parameter, value in parsed_body.items()}
