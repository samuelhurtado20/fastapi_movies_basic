from fastapi.responses import JSONResponse
from jwt import encode, decode, exceptions
import os


def create_token(data: dict) -> str:
    token: str = encode(payload=data,
                        key=os.getenv('SECRET_KEY'),
                        algorithm="HS256"
                        )
    return token


def validate_token(token: str) -> dict:
    try:
        print(token)
        print(os.getenv('SECRET_KEY'))
        resutl = decode(token, key=os.getenv('SECRET_KEY'), algorithms=["HS256"])
        print(resutl)
        return resutl
    except exceptions.DecodeError:
        return JSONResponse(content={"success": False, "message": "Invalid Token (DecodeError)"}, status_code=401)
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"success": False, "message": "Token Expired"}, status_code=401)
    except Exception as e:
        raise e
