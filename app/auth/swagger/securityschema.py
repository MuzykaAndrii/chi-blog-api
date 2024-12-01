SECURITY_SCHEMA = {
    "securityDefinitions": {
        "JWT Cookie": {
            "type": "apiKey",
            "in": "cookie",
            "name": "auth_token",
            "description": "JWT Token stored in cookies for authentication. Example: `auth_token=<JWT_TOKEN>`",
        }
    },
    "security": [{"JWT Cookie": []}],
}
