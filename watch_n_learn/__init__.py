__all__ = ["create_server"]

from secrets import token_urlsafe

from fastapi.applications import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from watch_n_learn.database.main import engine
from watch_n_learn.database.models import Base
from watch_n_learn.router.error import error_router
from watch_n_learn.router.get.guest import guest_get_router
from watch_n_learn.router.post.guest import guest_post_router

def create_server(debug__: bool) -> FastAPI:

    Base.metadata.create_all(engine)

    server = FastAPI(debug=debug__)

    server.add_middleware(SessionMiddleware, secret_key=token_urlsafe())

    @server.get("/ping")
    @server.head("/ping")
    def ping() -> None:

        return None

    server.include_router(guest_get_router)
    server.include_router(guest_post_router)

    server.mount("/static", StaticFiles(directory="watch_n_learn/static"))

    server.include_router(error_router)

    return server
