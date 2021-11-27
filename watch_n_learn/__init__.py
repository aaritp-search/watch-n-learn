__all__ = ["create_server"]

from fastapi.applications import FastAPI
from fastapi.staticfiles import StaticFiles

from watch_n_learn.router.error import error_router
from watch_n_learn.router.get.guest import guest_get_router

def create_server(debug__: bool) -> FastAPI:

    server = FastAPI(debug=debug__)

    @server.head("/ping")
    def ping() -> None:

        return None

    server.include_router(guest_get_router)

    server.mount("/static", StaticFiles(directory="watch_n_learn/static"))

    server.include_router(error_router)

    return server
