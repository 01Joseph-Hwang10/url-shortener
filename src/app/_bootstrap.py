from fastapi import FastAPI
from src.url_shortener import url_shortener_router


def bootstrap(app: FastAPI = None) -> FastAPI:
    app = app or FastAPI()

    app.include_router(url_shortener_router, prefix="")

    @app.get("/")
    async def root():
        return {"message": "OK"}

    return app
