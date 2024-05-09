from typing import List
from typing import Optional
from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Query
from fastapi.security import HTTPBearer
from sqlmodel import Session

from ..auth import AuthHandler
from ..dependencies import UserDependency, get_session
from ..models.helpers import set_attrs_from_dict
from ..models.services import ServiceCreate, ServiceRead, Service, ServiceUpdate, ServiceResponseModel, ServiceReject, \
    ServiceRate
from ..models.rates import Rate, RateRead
from ..models.favorites import Favorite
from ..repositories.service import find_all_services, find_service_by_id, find_services_for_user, save_service, \
    find_average_rate_for_service, find_user_rate_for_service, find_user_rate_approved_for_service, find_rates_for_service, find_user_rate_value_for_service
from ..repositories.service import get_filtered_services
from ..repositories.rate import save_rate, find_rate_by_id, find_rate_by_user_id_and_service_id
from ..repositories.user import find_user_by_id, find_user
from ..repositories.favorite import find_favorite_by_user_id_and_service_id, save_favorite, delete_favorite, is_service_faved_by_user

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
        services = find_services_for_user(session, user.id)
    else:
        services = find_all_services(session)
    for service in services:
        service.avg_rate = find_average_rate_for_service(session, service.id)

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

    service.avg_rate = find_average_rate_for_service(session, service.id)
    service.own_rate = find_user_rate_value_for_service(session, service.id, user.id)

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
        user_dependency: UserDependency,
        category_ids: Optional[List[int]] = Query(None, description="IDs de las categorías a filtrar"),
        user_ids: Optional[List[int]] = Query(None, description="IDs de los usuarios a filtrar"),
        user_lat: Optional[float] = Query(-34.5824, description="Latitud del usuario"),
        user_long: Optional[float] = Query(-58.4225, description="Longitud del usuario"),
        ordered_by_distance: Optional[bool] = Query(False, description="Ordenar por distancia"),
        ordered_by_availability_now: Optional[bool] = Query(False, description="Ordenar por disponibilidad actual"),
        availability_filter: Optional[bool] = Query(False, description="Filtrar por disponibilidad"),
        faved_only: Optional[bool] = Query(False, description="Filtrar por mis favoritos"),
        distance_filter: Optional[float] = Query(50.0, description="Filtrar por distancia en Km"),
        token: str = Depends(security),
        session: Session = Depends(get_session),
):
    auth_handler = AuthHandler()
    roles = auth_handler.get_roles_from_token(token)

    services = get_filtered_services(
        user_dependency, session, category_ids, user_ids, ordered_by_distance, ordered_by_availability_now, user_lat, user_long, roles,
        distance_filter, availability_filter, faved_only
    )

    response_models = [ServiceResponseModel(**{
        "id": service.id,
        "title": service.title,
        "description": service.description,
        "photo_url": service.photo_url,
        "availability_time_start": service.availability_time_start,
        "availability_time_end": service.availability_time_end,
        "availability_days": service.availability_days,
        "service_latitude": user_provider.address_lat,
        "service_longitude": user_provider.address_long,
        "service_avg_rate": find_average_rate_for_service(session, service.id),
        "user_id": user_provider.id,
        "user_name": user_provider.name,
        "user_surname": user_provider.surname,
        "user_profile_photo_url": user_provider.profile_photo_url,
        "user_phone_number": user_provider.phone_number,
        "distance": distance,
        "is_available": is_available,
        "own_rate": find_user_rate_value_for_service(session, service.id, user_dependency.id),
        "own_rate_approved": find_user_rate_approved_for_service(session, service.id, user_dependency.id),
        "faved_by_me": is_service_faved_by_user(session, service.id, user_dependency.id),
        "rates": find_rates_for_service(session, service.id),
    }) for service, user_provider, distance, is_available in services]

    return response_models


@router.post("/{id}/rate", status_code=200, response_model=ServiceRead)
def rate_service(
        id: int,
        service_rate: ServiceRate,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    user = find_user_by_id(session, user.id)
    if not user:
        raise HTTPException(status_code=400, detail='User not found')

    service = find_service_by_id(session, id)
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')

    rate = Rate(user_id=user.id, service_id=service.id, rate=service_rate.rate, message=service_rate.message,
                approved=None)
    save_rate(session, rate)
    service.avg_rate = find_average_rate_for_service(session, service.id)
    service.own_rate = find_user_rate_value_for_service(session, service.id, user.id)

    return service


@router.post("/{service_id}/rate/{rate_id}/approve", status_code=200, response_model=ServiceRead)
def approve_rate(
        service_id: int,
        rate_id: int,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    user = find_user_by_id(session, user.id)
    if not user:
        raise HTTPException(status_code=400, detail='User not found')

    service = find_service_by_id(session, service_id)
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')

    rate = find_rate_by_id(session, rate_id)
    rate.approved = True
    save_rate(session, rate)

    return service


@router.post("/{service_id}/rate/{rate_id}/reject", status_code=200, response_model=ServiceRead)
def reject_rate(
        service_id: int,
        rate_id: int,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    user = find_user_by_id(session, user.id)
    if not user:
        raise HTTPException(status_code=400, detail='User not found')

    service = find_service_by_id(session, service_id)
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')

    rate = find_rate_by_id(session, rate_id)
    rate.approved = False
    save_rate(session, rate)

    return service


@router.get("/{service_id}/rate/{user_mail}", status_code=200)
def get_service_rate(
        service_id: int,
        user_mail: str,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    service = find_service_by_id(session, service_id)

    user = find_user(session, user_mail)

    if not service:
        raise HTTPException(status_code=404, detail='Service not found')

    rate = find_rate_by_user_id_and_service_id(session, user.id, service_id)
    if not rate:
        raise HTTPException(status_code=404, detail='Rate not found')

    return rate


@router.post("/{id}/fav", status_code=200, response_model=ServiceRead)
def favorite_service(
        id: int,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    user = find_user_by_id(session, user.id)
    if not user:
        raise HTTPException(status_code=400, detail='User not found')

    service = find_service_by_id(session, id)
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')

    favorite = find_favorite_by_user_id_and_service_id(session, user.id, service.id)
    if not favorite:
        favorite = Favorite(user_id=user.id, service_id=service.id)
        save_favorite(session, favorite)

    return service


@router.post("/{id}/unfav", status_code=200, response_model=ServiceRead)
def unfavorite_service(
        id: int,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    user = find_user_by_id(session, user.id)
    if not user:
        raise HTTPException(status_code=400, detail='User not found')

    service = find_service_by_id(session, id)
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')

    favorite = find_favorite_by_user_id_and_service_id(session, user.id, service.id)
    if favorite:
        delete_favorite(session, favorite)

    return service