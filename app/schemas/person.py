from fastapi import Query
from typing import Optional
from pydantic import BaseModel
from typing import Annotated

class PersonBase(BaseModel):
    name: str
    age: Annotated[int | None, Query(ge=1, le=120)] = None
    address: str | None = None
    work: str | None = None

class PersonRequest(PersonBase):
    pass

class Person(PersonBase):
    id: int

class PersonUpdate(BaseModel):
    name: str | None = None
    age: Annotated[int | None, Query(ge=1, le=120)] = None
    address: str | None = None
    work: str | None = None
    