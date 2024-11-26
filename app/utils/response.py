from flask import Response


class JsonResponse(Response):
    """Shortcut class for json response"""

    default_mimetype: str = "application/json"
