import json
import os
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from jwt_manager import validate_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        auth: HTTPAuthorizationCredentials | None = await super().__call__(request)
        data = validate_token(auth.credentials)
        print(data.body.decode())
        result = json.loads(data.body.decode())
        print(result.get("message"))
        if data["email"] == None or data["email"] != "test@gmail.com":
            raise HTTPException(status_code=401, detail="Invalid crendentials")
