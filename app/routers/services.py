from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..dependencies import UserDependency, get_session
from ..models.services import ServiceCreate, ServiceRead, Service
from ..repositories.service import find_all, find_service_by_id
from ..repositories.user_repository import find_user_by_id

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


@router.get("/{service_id}", status_code=200, response_model=ServiceRead)
def get_service(
        service_id: int,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    service = find_service_by_id(session, service_id)
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')

    return service


@router.patch("/{id}", status_code=200, response_model=ServiceRead)
def update_service(
        id: int,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    raise HTTPException(status_code=500, detail='Not implemented')


@router.post("/", status_code=201, response_model=ServiceRead)
def create_service(
        service: ServiceCreate,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    user = find_user_by_id(session, user.id)
    if not user:
        raise HTTPException(status_code=400, detail='User not found')

    session.add(new_service := Service.from_orm(service))
    new_service.user_id = user.id
    new_service.approved = False
    session.commit()
    session.refresh(new_service)
    return new_service
