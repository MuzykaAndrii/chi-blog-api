from flask import Response
from pydantic import BaseModel


class DtoResponse(Response):
    """Shortcut response class for auto serializing pydantic-based DTO objects to json"""

    default_mimetype: str = "application/json"

    def __init__(self, response: BaseModel | None = None, *args, **kwargs):

        if isinstance(response, BaseModel):
            response = response.model_dump_json()

        super().__init__(response, *args, **kwargs)
