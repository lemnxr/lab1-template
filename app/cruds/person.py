from sqlalchemy.orm import Session

from models.person import PersonModel
from schemas.person import PersonRequest, PersonUpdate
from cruds.interfaces.person import IPersonCRUD


class PersonCRUD(IPersonCRUD):
    async def get_all(self):
        return self._db.query(PersonModel).all()

    async def get_by_id(self, person_id: int):
        return self._db.query(PersonModel).filter(PersonModel.id == person_id).first()

    async def add(self, person: PersonModel):
        try:
            self._db.add(person)
            self._db.commit()
            self._db.refresh(person)
        except:
            return None
        
        return person
    
    async def delete(self, person: PersonModel):
        self._db.delete(person)
        self._db.commit()
        
        return person

    async def patch(self, person: PersonModel, person_update: PersonUpdate):
        update_attributes = person_update.model_dump(exclude_unset=True)        

        for key, value in update_attributes.items():
            setattr(person, key, value)
        
        try:
            self._db.add(person)
            self._db.commit()
            self._db.refresh(person)
        except:
            return None
        
        return person
