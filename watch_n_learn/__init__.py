__all__ = ["create_server"]

from fastapi.applications import FastAPI

def create_server(debug__: bool) -> FastAPI:

    server = FastAPI(debug=debug__)

    return server
