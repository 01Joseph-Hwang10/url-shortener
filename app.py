import uvicorn
from fastapi import FastAPI
from src.routers import url_router
from src.config import Base, engine

app = FastAPI()

app.include_router(url_router, prefix="")


@app.get("/")
def root():
    return (
        "Welcome to the URL shortener API :) "
        "See the documentation at /docs or /redoc for more information."
    )


if __name__ == "__main__":
    # Creates the database tables
    Base.metadata.create_all(bind=engine)

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
