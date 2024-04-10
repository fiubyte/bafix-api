from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..dependencies import UserDependency, get_session
from ..models.helpers import set_attrs_from_dict
from ..models.services import ServiceCreate, ServiceRead, Service, ServiceUpdate
from ..repositories.service import find_all_services, find_service_by_id, find_services_for_user, save_service
from ..repositories.user_repository import find_user_by_id

router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[ServiceRead])
def get_services(
        user: UserDependency,
        session: Session = Depends(get_session),
        mine: bool = False
):
    if mine:
        return find_services_for_user(session, user.id)
    return find_all_services(session)


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
        service_update: ServiceUpdate,
        user: UserDependency,
        session: Session = Depends(get_session),
):
    service = find_service_by_id(session, id)
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')

    data_to_update_dict = service_update.dict(exclude_unset=True, exclude_none=True)
    set_attrs_from_dict(service, data_to_update_dict)
    save_service(session, service)
    return service


@router.post("/{id}/approve", status_code=200, response_model=ServiceRead)
def approve_service(
        id: int,
        user: UserDependency,
        session: Session = Depends(get_session),
):
    service = find_service_by_id(session, id)
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')

    service.approved = True
    save_service(session, service)
    return service


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
    save_service(session, new_service)
    return new_service
