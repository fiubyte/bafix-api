from typing import List, Any

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..dependencies import UserDependency, get_session
from ..models.services import ServiceCreate, ServiceRead

router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[ServiceRead])
async def get_services(
        user: UserDependency,
        session: Session = Depends(get_session)
):
    services = []
    return services


@router.patch("/{id}", response_model=ServiceRead, status_code=200)
async def update_service(
        id: int,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    return None


@router.post("/", response_model=ServiceRead, status_code=201)
async def create_service(
        service: ServiceCreate,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    return None
