from fastapi import FastAPI

from api.handlers import v1
from src.settings import settings

app = FastAPI()
app.include_router(router=v1.router, prefix="/api")


if __name__ == '__main__':
    from uvicorn import run
    run(
        app=app,
        host=settings.HOST,
        port=settings.PORT
    )
