from fastapi.templating import Jinja2Templates

from watch_n_learn.helper.function import get_flashed_messages

TEMPLATE = Jinja2Templates("watch_n_learn/template")

TEMPLATE.env.globals["get_flashed_messages"] = get_flashed_messages
