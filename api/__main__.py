from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from api.handlers import v1
from src.exception_handlers import request_validation_exception_handler
from src.settings import settings

app = FastAPI()
app.include_router(router=v1.router, prefix="/api")
app.add_exception_handler(
    exc_class_or_status_code=RequestValidationError,
    handler=request_validation_exception_handler  # noqa
)


if __name__ == '__main__':
    from uvicorn import run
    run(
        app=app,
        host=settings.HOST,
        port=settings.PORT
    )
