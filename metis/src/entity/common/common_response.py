from typing import Any
from sanic import json

from pydantic import BaseModel


class CommonResponse(BaseModel):
    status: str = 'success'
    messages: Any = None

    @staticmethod
    def success(messages: Any = None) -> 'CommonResponse':
        response = CommonResponse(status='success', messages=messages)
        return json(response.model_dump())
