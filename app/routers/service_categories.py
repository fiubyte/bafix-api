from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..dependencies import UserDependency, get_session
from ..models.service_categories import ServiceCategories

router = APIRouter(
    prefix="/service-categories",
    tags=["service-categories"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[ServiceCategories])
async def get_service_categories(
        user: UserDependency,
        session: Session = Depends(get_session)
):
    service_categories = []
    return service_categories