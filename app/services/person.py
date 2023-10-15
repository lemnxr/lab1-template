from sqlalchemy.orm import Session

from models.person import PersonModel
from schemas.person import PersonRequest, PersonUpdate
from cruds.person import PersonCRUD
from exceptions.exceptions import NotFoundException, ConflictException
from cruds.interfaces.person import IPersonCRUD


class PersonService():
    def __init__(self, personCRUD: type[IPersonCRUD], db: Session):
        self._personCRUD = personCRUD(db)
        
    async def get_all(self):
        return await self._personCRUD.get_all()

    async def get_by_id(self, person_id: int):
        person = await self._personCRUD.get_by_id(person_id)

        if person == None:
            raise NotFoundException(prefix="Get Person")
        return person
    
    async def add(self, person_request: PersonRequest):
        person = PersonModel(**person_request.model_dump())
        person = await self._personCRUD.add(person)
        if person == None:
            raise ConflictException(prefix="Add Person")
        return person
    
    async def delete(self, person_id: int):
        person = await self._personCRUD.get_by_id(person_id)

        if person == None:
            raise NotFoundException(prefix="Delete Person")
        return await self._personCRUD.delete(person)
    
    async def patch(self, person_id: int, person_update: PersonUpdate):
        person = await self._personCRUD.get_by_id(person_id)

        if person == None:
            raise NotFoundException(prefix="Update Person")
    
        person = await self._personCRUD.patch(person, person_update)

        if person == None:
            raise ConflictException(prefix="Update Person")
        return person
