from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[int] = None
    email: str = Field(min_length=5, max_length=25)
    password: str = Field(min_length=5, max_length=15)

    model_config = {
     "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "email": "example@email.com"
                }
            ]
        }
    }