LOGIN_USER = {
    "tags": ["Authentication"],
    "description": "Logs in a user and returns a JWT token in the response.",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "description": "User credentials (e.g., email and password)",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The email of the user",
                    },
                    "password": {
                        "type": "string",
                        "description": "The password of the user",
                    },
                },
                "required": ["email", "password"],
            },
        }
    ],
    "responses": {
        "200": {
            "description": "Login successful, returns JWT token",
            "content": {
                "application/json": {
                    "example": {
                        "token": "jwt_token_here",
                    }
                }
            },
        },
        "401": {
            "description": "Invalid credentials or authentication error",
            "content": {"application/json": {"example": {"error": "Invalid password"}}},
        },
    },
    "security": [{"JWT Cookie": []}],
}
