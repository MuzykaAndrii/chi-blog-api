GET_ROLES = {
    "tags": ["Roles"],
    "summary": "Get all roles",
    "description": "Retrieve a list of all roles in the system, including their permissions.",
    "responses": {
        "200": {
            "description": "A list of roles",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "admin",
                            "permissions": [{"id": 1, "name": "permissions.can_view"}],
                        },
                        {"id": 2, "name": "viewer", "permissions": []},
                    ]
                }
            },
        },
        "401": {"description": "Unauthorized. User not authenticated."},
        "403": {"description": "Forbidden. User lacks necessary permission."},
    },
}

GET_ROLE = {
    "tags": ["Roles"],
    "summary": "Get a single role by ID",
    "description": "Fetch details of a specific role by its ID.",
    "parameters": [
        {
            "name": "role_id",
            "in": "path",
            "required": True,
            "description": "ID of the role to fetch",
            "schema": {"type": "integer"},
        }
    ],
    "responses": {
        "200": {
            "description": "Details of the role",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "admin",
                        "permissions": [{"id": 1, "name": "permissions.can_view"}],
                    }
                }
            },
        },
        "404": {"description": "Role not found"},
        "401": {"description": "Unauthorized. User not authenticated."},
        "403": {"description": "Forbidden. User lacks necessary permission."},
    },
}

CREATE_ROLE = {
    "tags": ["Roles"],
    "summary": "Create a new role",
    "description": "Create a new role with the specified permissions.",
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "example": {"name": "moderator", "permissions": [{"id": 1}]}
            }
        },
    },
    "responses": {
        "201": {
            "description": "Role created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 3,
                        "name": "moderator",
                        "permissions": [{"id": 1}],
                    }
                }
            },
        },
        "409": {"description": "Conflict. Role with this name already exists."},
        "401": {"description": "Unauthorized. User not authenticated."},
        "403": {"description": "Forbidden. User lacks necessary permission."},
    },
}

UPDATE_ROLE = {
    "tags": ["Roles"],
    "summary": "Update an existing role",
    "description": "Update an existing role's details, including its permissions.",
    "parameters": [
        {
            "name": "role_id",
            "in": "path",
            "required": True,
            "description": "ID of the role to update",
            "schema": {"type": "integer"},
        }
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "example": {"name": "admin", "permissions": [{"id": 1}, {"id": 2}]}
            }
        },
    },
    "responses": {
        "200": {
            "description": "Role updated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "admin",
                        "permissions": [{"id": 1}, {"id": 2}],
                    }
                }
            },
        },
        "404": {"description": "Role not found"},
        "409": {"description": "Conflict. Role name already exists."},
        "401": {"description": "Unauthorized. User not authenticated."},
        "403": {"description": "Forbidden. User lacks necessary permission."},
    },
}

DELETE_ROLE = {
    "tags": ["Roles"],
    "summary": "Delete an existing role",
    "description": "Delete an existing role from the system.",
    "parameters": [
        {
            "name": "role_id",
            "in": "path",
            "required": True,
            "description": "ID of the role to delete",
            "schema": {"type": "integer"},
        }
    ],
    "responses": {
        "204": {"description": "Role deleted successfully"},
        "404": {"description": "Role not found"},
        "401": {"description": "Unauthorized. User not authenticated."},
        "403": {"description": "Forbidden. User lacks necessary permission."},
    },
}

ASSIGN_PERMISSION_TO_ROLE = {
    "tags": ["Roles"],
    "summary": "Assign a permission to a role",
    "description": "Assign a specific permission to a role. This allows the role to gain access to the functionality associated with that permission.",
    "parameters": [
        {
            "name": "role_id",
            "in": "path",
            "required": True,
            "description": "ID of the role to which the permission will be assigned",
            "schema": {"type": "integer"},
        },
        {
            "name": "permission_id",
            "in": "path",
            "required": True,
            "description": "ID of the permission to assign",
            "schema": {"type": "integer"},
        },
    ],
    "responses": {
        "200": {
            "description": "Permission successfully assigned to the role",
            "content": {
                "application/json": {
                    "example": {"message": "Permission assigned successfully."}
                }
            },
        },
        "404": {"description": "Role or permission not found"},
        "400": {"description": "Bad Request. Invalid role or permission ID"},
        "401": {"description": "Unauthorized. User not authenticated."},
        "403": {"description": "Forbidden. User lacks necessary permission."},
    },
}

REMOVE_PERMISSION_FROM_ROLE = {
    "tags": ["Roles"],
    "summary": "Remove a permission from a role",
    "description": "Remove a specific permission from a role. This revokes the functionality associated with that permission from the role.",
    "parameters": [
        {
            "name": "role_id",
            "in": "path",
            "required": True,
            "description": "ID of the role from which the permission will be removed",
            "schema": {"type": "integer"},
        },
        {
            "name": "permission_id",
            "in": "path",
            "required": True,
            "description": "ID of the permission to remove",
            "schema": {"type": "integer"},
        },
    ],
    "responses": {
        "200": {
            "description": "Permission successfully removed from the role",
            "content": {
                "application/json": {
                    "example": {"message": "Permission removed successfully."}
                }
            },
        },
        "404": {"description": "Role or permission not found"},
        "400": {"description": "Bad Request. Invalid role or permission ID"},
        "401": {"description": "Unauthorized. User not authenticated."},
        "403": {"description": "Forbidden. User lacks necessary permission."},
    },
}

GET_ROLE_PERMISSIONS = {
    "tags": ["Roles"],
    "summary": "Get all permissions assigned to a role",
    "description": "Retrieve a list of all permissions assigned to a specific role.",
    "parameters": [
        {
            "name": "role_id",
            "in": "path",
            "required": True,
            "description": "ID of the role to get permissions for",
            "schema": {"type": "integer"},
        }
    ],
    "responses": {
        "200": {
            "description": "A list of permissions assigned to the role",
            "content": {
                "application/json": {
                    "example": [
                        {"id": 1, "name": "permissions.can_view"},
                        {"id": 2, "name": "permissions.can_create"},
                    ]
                }
            },
        },
        "404": {"description": "Role not found"},
        "401": {"description": "Unauthorized. User not authenticated."},
        "403": {"description": "Forbidden. User lacks necessary permission."},
    },
}
