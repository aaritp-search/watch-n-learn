from datetime import timedelta
from secrets import token_urlsafe
from typing import Optional

from fastapi_login.fastapi_login import LoginManager

from watch_n_learn.database.main import session
from watch_n_learn.database.models import User

manager = LoginManager(token_urlsafe(), "/internal/login", default_expiry=timedelta(hours=2.0))

@manager.user_loader()
def get_user(username__: str) -> Optional[User]:

    return session.query(User).filter_by(username=username__).first()
