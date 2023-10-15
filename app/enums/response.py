from enum import Enum

from schemas.person import Person
from schemas.response import ErrorResponse, ValidationErrorResponse

class ResponseClass(Enum):
    GetAll = {
        "model": list[Person],
        "description": "All Persons",
    }
    GetByID = {
        "model": Person,
        "description": "Person by ID",
    }
    Add = {
        "description": "Add new Person",
        "headers": {
            "Location": {
                "description": "Path to new Person",
                "style": "simple",
                "schema": {
                    "type": "string"
                }
            }
        },
        "content": {
            "application/octet-stream": {
                "example": ""
            }
        },
    }
    Delete = {
        "description": "Person by ID was deleted",
        "content": {
            "application/octet-stream": {
                "example": ""
            }
        },
    }
    Patch = {
        "model": Person,
        "description": "Person by ID was updated",
    }


    InvalidData = {
        "model": ValidationErrorResponse,
        "description": "Invalid data",
    }
    NotFound = {
        "model": ErrorResponse,
        "description": "Not found Person by ID",
    }
    Conflict = {
        "model": ErrorResponse,
        "description": "Conflict",
    }
    