from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..dependencies import UserDependency, get_session
from ..models.service_categories import ServiceCategory
from ..repositories.service_categories import find_all_service_categories

router = APIRouter(
    prefix="/service-categories",
    tags=["service-categories"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[ServiceCategory], status_code=200)
async def get_service_categories(
        user: UserDependency,
        session: Session = Depends(get_session)
):
    service_categories = find_all_service_categories(session)
    return service_categories
