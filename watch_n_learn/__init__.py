__all__ = ["create_server"]

from fastapi.applications import FastAPI

from watch_n_learn.router.error import error_router

def create_server(debug__: bool) -> FastAPI:

    server = FastAPI(debug=debug__)

    @server.head("/ping")
    def ping() -> None:

        return None

    server.include_router(error_router)

    return server
