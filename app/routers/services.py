from typing import List
from tabulate import tabulate
from pprint import pprint
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, or_
from typing import Optional
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func
from sqlalchemy import func
from sqlalchemy.sql.expression import cast
from sqlalchemy.types import Float

from ..repositories.service import get_filtered_services




from ..dependencies import UserDependency, get_session
from ..models.services import ServiceCreate, ServiceRead, Service, ServiceResponseModel
from ..repositories.service import find_all, find_service_by_id, find_services_for_user
from ..repositories.user_repository import find_user_by_id

from math import radians, sin, cos, sqrt, atan2
from ..models.services import Service
from ..models.users import User

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
    return find_all(session)


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

@router.get("/filter/", response_model=List[ServiceResponseModel])
def get_services(
    category_ids: Optional[List[int]] = Query(None, description="IDs de las categorías a filtrar"),
    user_ids: Optional[List[int]] = Query(None, description="IDs de los usuarios a filtrar"),
    days: Optional[List[str]] = Query(None, description="Días de la semana a filtrar"),
    distance: Optional[int] = Query(300000000, description="Distancia máxima en metros"),
    user_lat: float = Query(-34.5824, description="Latitud del usuario"),
    user_long: float = Query(-58.4225, description="Longitud del usuario"),
    check_time: Optional[str] = Query(None, description="Hora a chequear disponibilidad (HH:MM)"),
    session: Session = Depends(get_session)
):
    services = get_filtered_services(session, category_ids, user_ids, days, distance, user_lat, user_long, check_time)
    
    response_models = [ServiceResponseModel(**{
        "id": service.id,
        "title": service.title,
        "description": service.description,
        "photo_url": service.photo_url,
        "availability_time_start": service.availability_time_start,
        "availability_time_end": service.availability_time_end,
        "availability_days": service.availability_days,
        "service_latitude": user_address_lat,  
        "service_longitude": user_address_long,
    }) for service, user_name, user_email, user_address, user_address_lat, user_address_long, User_approved in services]

    return response_models
