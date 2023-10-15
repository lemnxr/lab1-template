from copy import deepcopy

from mocks.person import PersonMockCRUD, PersonDataMock
from services.person import PersonService
from schemas.person import Person, PersonRequest, PersonUpdate
from models.person import PersonModel
from exceptions.exceptions import NotFoundException, ConflictException


personService = PersonService(
    personCRUD=PersonMockCRUD,
    db=None
)
correct_persons = deepcopy(PersonDataMock._persons)

print(correct_persons)


def model_into_dict(personModel: PersonModel) -> dict:
    person = personModel.__dict__
    del person["_sa_instance_state"]
    return person


async def test_get_all_success():
    try:
        persons = await personService.get_all()

        assert len(persons) == len(correct_persons)
        for i in range(len(persons)):
            assert model_into_dict(persons[i]) == correct_persons[i]
    except:
        assert False


async def test_get_by_id_success():
    try:
        person = await personService.get_by_id(2)

        correct_person = PersonDataMock._persons[1]
        assert model_into_dict(person) == correct_person
    except:
        assert False


async def test_get_by_id_not_found():
    try:
        await personService.get_by_id(10)

        assert False
    except NotFoundException:
        assert True
    except:
        assert False


async def test_add_success():
    try:
        person = await personService.add(
            PersonRequest(
                name="Test person",
                age=25,
                address="Test address",
                work="developer"
            )
        )
        
        assert person.name == "Test person"
    except:
        assert False


async def test_add_conflict_name():
    try:
        await personService.add(
            PersonRequest(
                name="Name1",
                age=25,
                address="Test address",
                work="developer"
            )
        )
        
        assert False
    except ConflictException:
        assert True
    except:
        assert False


async def test_delete_success():
    try:
        person = await personService.delete(1)

        assert correct_persons[0] == model_into_dict(person)
    except:
        assert False


async def test_delete_not_found():
    try:
        await personService.delete(10)
        
        assert False
    except NotFoundException:
        assert True
    except:
        assert False


async def test_patch_success():
    try:
        person = await personService.patch(person_id=2, person_update=PersonUpdate(age=22, work="NewWork"))
        
        correct_person = deepcopy(correct_persons[1])
        correct_person["age"] = 22
        correct_person["work"] = "NewWork"
        assert correct_person == model_into_dict(person)
    except:
        assert False


async def test_patch_not_found():
    try:
        await personService.patch(person_id=10, person_update=PersonUpdate(age=22, work="NewWork"))
        assert False
    except NotFoundException:
        assert True
    except:
        assert False


async def test_patch_conflict():
    try:
        await personService.patch(person_id=3, person_update=PersonUpdate(name="Name4"))
        assert False
    except ConflictException:
        assert True
    except:
        assert False
