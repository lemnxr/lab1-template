from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from sqlalchemy.orm import session
from typing import Annotated

from models.person import PersonModel
from config.db_connect import DB
from enums.response import ResponseClass
from services.person import PersonService
from schemas.person import PersonRequest, PersonUpdate
from cruds.interfaces.person import IPersonCRUD
from cruds.person import PersonCRUD
from mocks.person import PersonMockCRUD

def get_person_crud() -> type[IPersonCRUD]:
    return PersonCRUD

router = APIRouter(
    prefix="/persons",
    tags=["Person API"],
    responses={
        status.HTTP_400_BAD_REQUEST: ResponseClass.InvalidData.value
    }
)

person_database = DB()


@router.get("/", status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponseClass.GetAll.value
            })
async def get_all(personCRUD: Annotated[IPersonCRUD, Depends(get_person_crud)],
                    db: session = Depends(person_database.get_db)):
    return await PersonService(personCRUD=personCRUD, db=db).get_all()


@router.get("/{person_id}", status_code=status.HTTP_200_OK,
            responses={
                status.HTTP_200_OK: ResponseClass.GetByID.value,
                status.HTTP_404_NOT_FOUND: ResponseClass.NotFound.value
            })
async def get_by_id(personCRUD: Annotated[IPersonCRUD, Depends(get_person_crud)],
                    id: int,
                    db: session = Depends(person_database.get_db)):
    return await PersonService(personCRUD=personCRUD, db=db).get_by_id(id)


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_class=Response,
             responses={
                 status.HTTP_201_CREATED: ResponseClass.Add.value,
                 status.HTTP_409_CONFLICT: ResponseClass.Conflict.value
             })
async def add(personCRUD: Annotated[IPersonCRUD, Depends(get_person_crud)],
              person_request: PersonRequest,
              db: session = Depends(person_database.get_db)):
    await PersonService(personCRUD=personCRUD,db=db).add(person_request)
    return Response(status_code=status.HTTP_201_CREATED)
    

@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT,
               response_class=Response,
               responses={
                   status.HTTP_204_NO_CONTENT: ResponseClass.Delete.value,
                   status.HTTP_404_NOT_FOUND: ResponseClass.Delete.value
               })
async def delete(personCRUD: Annotated[IPersonCRUD, Depends(get_person_crud)],
                 id: int,
                 db: session = Depends(person_database.get_db)):
    await PersonService(personCRUD=personCRUD,db=db).delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{person_id}", status_code=status.HTTP_200_OK,
              responses={
                  status.HTTP_200_OK: ResponseClass.Patch.value,
                  status.HTTP_404_NOT_FOUND: ResponseClass.NotFound.value,
                  status.HTTP_409_CONFLICT: ResponseClass.Conflict.value
              })
async def patch(personCRUD: Annotated[IPersonCRUD, Depends(get_person_crud)],
                id: int,
                person_update: PersonUpdate,
                db: session = Depends(person_database.get_db)):
    return await PersonService(personCRUD=personCRUD,db=db).patch(id, person_update)
