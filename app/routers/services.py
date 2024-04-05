from typing import List, Any

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..dependencies import UserDependency, get_session
from ..models.services import ServiceCreate, ServiceRead, Service
from ..repositories.service import find_all

router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[ServiceRead])
def get_services(
        user: UserDependency,
        session: Session = Depends(get_session)
):
    services = find_all(session)
    return services


@router.patch("/{id}", response_model=ServiceRead, status_code=200)
def update_service(
        id: int,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    return None


@router.post("/", response_model=ServiceRead, status_code=201)
def create_service(
        service: ServiceCreate,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    session.add(new_service := Service.from_orm(service))
    new_service.user_id = user.id
    session.commit()
    session.refresh(new_service)
    return new_service
