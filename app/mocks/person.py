from models.person import PersonModel
from schemas.person import PersonRequest, PersonUpdate
from mocks.data import PersonDataMock
from cruds.interfaces.person import IPersonCRUD

class PersonMockCRUD(IPersonCRUD, PersonDataMock):
    async def get_all(self) -> list[PersonModel]:
        persons = [PersonModel(**item) for item in self._persons]
        return persons

    async def get_by_id(self, person_id: int) -> PersonModel | None:
        for item in self._persons:
            if item["id"] == person_id:
                return PersonModel(**item)
        return None
    
    async def add(self, person: PersonModel) -> PersonModel | None:
        for item in self._persons:
            if item["name"] == person.name:
                return None
            
        self._persons.append(
            {
                "id": 1 if len(self._persons) == 0 
                        else self._persons[-1]["id"] + 1,
                "name": person.name,
                "age": person.age,
                "address": person.address,
                "work": person.work
            },
        )
        return PersonModel(**self._persons[-1])
    
    async def delete(self, person: PersonModel) -> PersonModel:
        for i in range(len(self._persons)):
            item = self._persons[i]
            if item["id"] == person.id:
                deleted_person = self._persons.pop(i)
                break
                
        return PersonModel(**deleted_person)

    async def patch(
            self, 
            person: PersonModel, 
            person_update: PersonUpdate
        ) -> PersonModel | None:
            
        for item in self._persons:
            if item["id"] != person.id and \
                item["name"] == person_update.name:
                return None
        
        update_fields = person_update.model_dump(exclude_unset=True) 
        for item in self._persons:
            if item["id"] == person.id:
                for key in update_fields:
                    item[key] = update_fields[key]

                updated_person = PersonModel(**item)
                break
        return updated_person
