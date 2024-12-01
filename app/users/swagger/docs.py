GET_USERS_LIST = {
    "tags": ["Users"],
    "summary": "Retrieve list of users",
    "description": "Retrieve all users or search users by name",
    "parameters": [
        {
            "name": "name",
            "in": "query",
            "type": "string",
            "required": False,
            "description": "Optional search term to filter users by name",
        }
    ],
    "responses": {
        "200": {
            "description": "Successfully retrieved users list",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "username": {"type": "string"},
                        "email": {"type": "string"},
                        "role": {"type": "string"},
                    },
                },
            },
        }
    },
}

GET_USER = {
    "tags": ["Users"],
    "summary": "Retrieve a specific user",
    "description": "Get user details by user ID",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "The unique identifier of the user",
        }
    ],
    "responses": {
        "200": {
            "description": "Successfully retrieved user details",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "username": {"type": "string"},
                    "email": {"type": "string"},
                    "role": {"type": "string"},
                },
            },
        },
        "404": {"description": "User not found"},
    },
}

CREATE_USER = {
    "tags": ["Users"],
    "summary": "Create a new user",
    "description": "Create a new user with provided details",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["username", "email", "password"],
                "properties": {
                    "username": {"type": "string"},
                    "email": {"type": "string"},
                    "password": {"type": "string"},
                    "role_id": {"type": "integer"},
                },
            },
        }
    ],
    "responses": {
        "201": {
            "description": "User successfully created",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "username": {"type": "string"},
                    "email": {"type": "string"},
                    "role": {"type": "string"},
                },
            },
        },
        "400": {"description": "Validation error or user already exists"},
    },
    "security": [{"JWT Cookie": []}],
}

UPDATE_USER = {
    "tags": ["Users"],
    "summary": "Update an existing user",
    "description": "Update user details by user ID",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "The unique identifier of the user to update",
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "email": {"type": "string"},
                    "password": {"type": "string"},
                    "role_id": {"type": "integer"},
                },
            },
        },
    ],
    "responses": {
        "200": {
            "description": "User successfully updated",
            "schema": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "username": {"type": "string"},
                    "email": {"type": "string"},
                    "role": {"type": "string"},
                },
            },
        },
        "400": {"description": "Validation error"},
        "404": {"description": "User not found"},
    },
    "security": [{"JWT Cookie": []}],
}

DELETE_USER = {
    "tags": ["Users"],
    "summary": "Delete a user",
    "description": "Delete user by user ID",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "The unique identifier of the user to delete",
        }
    ],
    "responses": {
        "204": {"description": "User successfully deleted"},
        "404": {"description": "User not found"},
    },
    "security": [{"JWT Cookie": []}],
}
