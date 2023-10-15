from fastapi import APIRouter

from routers import person

router = APIRouter()
router.include_router(person.router)
