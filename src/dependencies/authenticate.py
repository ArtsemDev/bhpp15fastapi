from fastapi import Depends, Header, HTTPException
from fastapi.requests import Request
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from src.database import User
from src.dependencies.database_session import DBAsyncSession
from src.settings import jwt_manager

__all__ = ["authenticate"]


async def _authenticate(request: Request, db_session: DBAsyncSession, authorization: str = Header(default=None)):
    if authorization is None:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN
        )

    payload = jwt_manager.verify_access_token(token=authorization)
    print(payload)
    user = await db_session.get(entity=User, ident=payload.get("sub"))
    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND
        )

    request.scope["state"]["user"] = user


authenticate = Depends(dependency=_authenticate)
