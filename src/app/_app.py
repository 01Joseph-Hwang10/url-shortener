from fastapi import FastAPI
from src.url_shortener import url_shortener_router

app = FastAPI()

app.include_router(url_shortener_router, prefix="")


@app.get("/")
def root():
    return {"message": "OK"}
