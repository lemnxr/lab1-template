from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

from models.person import PersonModel
from schemas.person import PersonRequest, PersonUpdate


class IPersonCRUD(ABC):
    def __init__(self, db: Session):
        self._db = db

    @abstractmethod
    async def get_all(self) -> list[PersonModel]:
       pass
    
    @abstractmethod
    async def get_by_id(self, person_id: int) -> PersonModel | None:
        pass

    @abstractmethod
    async def add(self, person: PersonModel) -> PersonModel | None:
        pass
    
    @abstractmethod
    async def delete(self, person: PersonModel) -> PersonModel:
        pass
    
    @abstractmethod
    async def patch(self, person: PersonModel, person_update: PersonUpdate) -> PersonModel | None:
        pass
