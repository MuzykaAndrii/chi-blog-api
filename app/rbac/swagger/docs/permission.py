GET_PERMISSIONS = {
    "tags": ["Permissions"],
    "summary": "Get all permissions",
    "description": "Returns a list of all permissions available in the system.",
    "responses": {
        "200": {
            "description": "A list of permissions",
            "content": {
                "application/json": {
                    "example": [
                        {"id": 1, "name": "permissions.can_view"},
                        {"id": 2, "name": "permissions.can_create"},
                    ]
                }
            },
        },
        "401": {"description": "Unauthorized. User not authenticated."},
        "403": {"description": "Forbidden. User lacks necessary permission."},
    },
}

GET_PERMISSION = {
    "tags": ["Permissions"],
    "summary": "Get a single permission by ID",
    "description": "Fetch details of a specific permission by its ID.",
    "parameters": [
        {
            "name": "permission_id",
            "in": "path",
            "required": True,
            "description": "ID of the permission to fetch",
            "schema": {"type": "integer"},
        }
    ],
    "responses": {
        "200": {
            "description": "Details of the permission",
            "content": {
                "application/json": {
                    "example": {"id": 1, "name": "permissions.can_view"}
                }
            },
        },
        "404": {"description": "Permission not found"},
        "401": {"description": "Unauthorized. User not authenticated."},
        "403": {"description": "Forbidden. User lacks necessary permission."},
    },
}

CREATE_PERMISSION = {
    "tags": ["Permissions"],
    "summary": "Create a new permission",
    "description": "Create a new permission in the system.",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {"example": {"name": "permissions.can_delete"}}
        },
    },
    "responses": {
        "201": {
            "description": "Permission created successfully",
            "content": {
                "application/json": {
                    "example": {"id": 3, "name": "permissions.can_delete"}
                }
            },
        },
        "409": {"description": "Conflict. Permission with this name already exists."},
        "401": {"description": "Unauthorized. User not authenticated."},
        "403": {"description": "Forbidden. User lacks necessary permission."},
    },
}

UPDATE_PERMISSION = {
    "tags": ["Permissions"],
    "summary": "Update an existing permission",
    "description": "Update the details of an existing permission.",
    "parameters": [
        {
            "name": "permission_id",
            "in": "path",
            "required": True,
            "description": "ID of the permission to update",
            "schema": {"type": "integer"},
        }
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {"example": {"name": "permissions.can_update"}}
        },
    },
    "responses": {
        "200": {
            "description": "Permission updated successfully",
            "content": {
                "application/json": {
                    "example": {"id": 1, "name": "permissions.can_update"}
                }
            },
        },
        "404": {"description": "Permission not found"},
        "409": {"description": "Conflict. Permission with this name already exists."},
        "401": {"description": "Unauthorized. User not authenticated."},
        "403": {"description": "Forbidden. User lacks necessary permission."},
    },
}

DELETE_PERMISSION = {
    "tags": ["Permissions"],
    "summary": "Delete an existing permission",
    "description": "Delete an existing permission from the system.",
    "parameters": [
        {
            "name": "permission_id",
            "in": "path",
            "required": True,
            "description": "ID of the permission to delete",
            "schema": {"type": "integer"},
        }
    ],
    "responses": {
        "204": {"description": "Permission deleted successfully"},
        "404": {"description": "Permission not found"},
        "401": {"description": "Unauthorized. User not authenticated."},
        "403": {"description": "Forbidden. User lacks necessary permission."},
    },
}
