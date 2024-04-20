from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from fastapi import Query
from typing import Optional
from ..auth import AuthHandler
from fastapi.security import HTTPBearer
from datetime import datetime
import pytz



from ..dependencies import UserDependency, get_session
from ..models.helpers import set_attrs_from_dict
from ..models.services import ServiceCreate, ServiceRead, Service, ServiceUpdate, ServiceResponseModel, ServiceReject
from ..repositories.service import find_all_services, find_service_by_id, find_services_for_user, save_service
from ..repositories.user_repository import find_user_by_id
from ..repositories.service import get_filtered_services

router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={404: {"description": "Not found"}},
)
security = HTTPBearer()


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

@router.post("/{id}/reject", status_code=200, response_model=ServiceRead)
def reject_service(
        id: int,
        service_reject: ServiceReject,
        user: UserDependency,
        session: Session = Depends(get_session),
):
    service = find_service_by_id(session, id)
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')

    service.approved = False
    service.rejected_message = service_reject.rejected_message
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
    new_service.approved = None
    save_service(session, new_service)
    return new_service


@router.get("/filter/", response_model=List[ServiceResponseModel])
def get_services(
    category_ids: Optional[List[int]] = Query(None, description="IDs de las categorías a filtrar"),
    user_ids: Optional[List[int]] = Query(None, description="IDs de los usuarios a filtrar"),
    user_lat: Optional[float] = Query(-34.5824, description="Latitud del usuario"),
    user_long: Optional[float] = Query(-58.4225, description="Longitud del usuario"),
    ordered_by_distance: Optional[bool] = Query(False, description="Ordenar por distancia"),
    ordered_by_availability_now: Optional[bool] = Query(False, description="Ordenar por disponibilidad actual"),
    availability_filter: Optional[bool] = Query(False, description="Filtrar por disponibilidad"),
    distance_filter: Optional[float] = Query(50.0, description="Filtrar por distancia en Km"),
    token: str = Depends(security),
    session: Session = Depends(get_session)
):
    auth_handler = AuthHandler()
    roles = auth_handler.get_roles_from_token(token)

    services = get_filtered_services(
        session, category_ids, user_ids, ordered_by_distance, ordered_by_availability_now, user_lat, user_long, roles, distance_filter, availability_filter
    )

    response_models = [ServiceResponseModel(**{
        "id": service.id,
        "title": service.title,
        "description": service.description,
        "photo_url": service.photo_url,
        "availability_time_start": service.availability_time_start,
        "availability_time_end": service.availability_time_end,
        "availability_days": service.availability_days,
        "service_latitude": user.address_lat,
        "service_longitude": user.address_long,
        "user_id": user.id,
        "user_name": user.name,
        "user_surname": user.surname,
        "user_profile_photo_url": user.profile_photo_url,
        "user_phone_number": user.phone_number,
        "distance": distance,
        "is_available": is_available
    }) for service, user, distance, is_available in services]

    return response_models