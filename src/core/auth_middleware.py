from fastapi import HTTPException, Header

from os import getenv
from jose import jwt
from typing import Annotated

from utils import auth_token


async def auth(authorization: Annotated[str | None, Header()] = None):
    if not authorization:
        return auth_token.generate_token()

    try:
        scheme, token = authorization.split()

        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")

        payload = jwt.decode(token, getenv('JWT_SECRET_KEY'), algorithms=[getenv('JWT_ALGORITHM')])
        identifier: str = payload.get("sub")

        if not identifier:
            raise HTTPException(status_code=401)

    except Exception as e:
        token: str = auth_token.generate_token()


        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Invalid or expired token.",
        # )

    return token

