from fastapi import FastAPI

from api.handlers import v1

app = FastAPI()
app.include_router(router=v1.router, prefix="/api")


if __name__ == '__main__':
    from uvicorn import run
    run(app=app)
