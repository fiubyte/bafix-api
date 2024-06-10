from datetime import datetime
from typing import List
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi import Query
from fastapi.security import HTTPBearer
from sqlmodel import Session

from ..auth import AuthHandler
from ..dependencies import UserDependency, get_session
from ..models.favorites import Favorite
from ..models.helpers import set_attrs_from_dict
from ..models.rates import Rate
from ..models.service_contact import ServiceContact
from ..models.service_view import ServiceView
from ..models.services import ServiceCreate, ServiceRead, Service, ServiceUpdate, ServiceResponseModel, ServiceReject, \
    ServiceRate
from ..repositories.favorite import find_favorite_by_user_id_and_service_id, save_favorite, delete_favorite, \
    is_service_faved_by_user
from ..repositories.rate import save_rate, find_rate_by_id, find_rate_by_user_id_and_service_id, delete_rate
from ..repositories.service import find_all_services, find_service_by_id, find_services_for_user, save_service, \
    find_average_rate_for_service, find_user_rate_approved_for_service, find_rates_for_service, \
    find_user_rate_value_for_service
from ..repositories.service import get_filtered_services, find_top_services_with_weighted_score
from ..repositories.service_contact import save_service_contact, find_service_contacts, find_top_contacts_users
from ..repositories.service_view import save_service_view, find_service_views
from ..repositories.user import find_user_by_id, find_user

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
        user_dependency, session, category_ids, user_ids, ordered_by_distance, ordered_by_availability_now, user_lat,
        user_long, roles,
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
        session: Session = Depends(get_session),
        user_name_to_display: Optional[str] = Query("NombreDefault", description="Optional"),
):
    user = find_user_by_id(session, user.id)
    if not user:
        raise HTTPException(status_code=400, detail='User not found')

    service = find_service_by_id(session, id)
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')
    rate = find_rate_by_user_id_and_service_id(session, user.id, service.id)
    if rate is not None:
        delete_rate(session, rate)

    rate = Rate(user_id=user.id, service_id=service.id, rate=service_rate.rate, message=service_rate.message,
                approved=None, user_name_to_display=user_name_to_display, user_email=user.email)

    save_rate(session, rate)
    service.avg_rate = find_average_rate_for_service(session, service.id)
    service.own_rate = find_user_rate_value_for_service(session, service.id, user.id)
    service.own_rate_approved = find_user_rate_approved_for_service(session, service.id, user.id)

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

    service.own_rate_approved = False
    save_service(session, service)
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


@router.post("/{id}/view", status_code=200)
def view_service(
        id: int,
        user: UserDependency,
        session: Session = Depends(get_session),
):
    user = find_user_by_id(session, user.id)
    if not user:
        raise HTTPException(status_code=400, detail='User not found')

    service = find_service_by_id(session, id)
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')

    save_service_view(session, ServiceView(user_id=user.id, service_id=service.id, timestamp=datetime.now()))

    return


@router.get("/{id}/view", status_code=200)
def get_service_views(
        id: int,
        user: UserDependency,
        session: Session = Depends(get_session),
):
    user = find_user_by_id(session, user.id)
    if not user:
        raise HTTPException(status_code=400, detail='User not found')

    service = find_service_by_id(session, id)
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')

    return find_service_views(session, service.id)


@router.post("/{id}/contact", status_code=200)
def contact_service(
        id: int,
        user: UserDependency,
        session: Session = Depends(get_session),
):
    user = find_user_by_id(session, user.id)
    if not user:
        raise HTTPException(status_code=400, detail='User not found')

    service = find_service_by_id(session, id)
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')

    save_service_contact(session, ServiceContact(user_id=user.id, service_id=service.id, timestamp=datetime.now()))

    return


@router.get("/{id}/contact", status_code=200)
def get_service_contacts(
        id: int,
        user: UserDependency,
        session: Session = Depends(get_session),
):
    user = find_user_by_id(session, user.id)
    if not user:
        raise HTTPException(status_code=400, detail='User not found')

    service = find_service_by_id(session, id)
    if not service:
        raise HTTPException(status_code=404, detail='Service not found')

    return find_service_contacts(session, service.id)

@router.get("/metrics/top_contacts/")
def get_top_contacts(
    session: Session = Depends(get_session),
    start_date: datetime = Query(default=datetime(2000,1,1), description="Start date for the range of dates in ISO 8601 format"),
    end_date: datetime = Query(default=datetime(2025,1,1), description="End date for the range of dates in ISO 8601 format")
):
    response = []
    contacts = find_top_contacts_users(session, start_date, end_date)
    
    for contact in contacts:
        print(contact)
        
        user_id = contact["user_id"]
        user = find_user_by_id(session, user_id)
        response.append({"user_id": user.id, "user_name": user.name, "user_surname": user.surname, "photo_url": user.profile_photo_url, "contacts": contact[1]})

    
    if not contacts:
        raise HTTPException(status_code=404, detail="No contact data found for the specified range and grouping option.")

    return response

@router.get("/metrics/top_services/")
def get_top_services(
    session: Session = Depends(get_session),
    start_date: datetime = Query(default=datetime(2000,1,1), description="Start date for the range of dates in ISO 8601 format"),
    end_date: datetime = Query(default=datetime(2025,1,1), description="End date for the range of dates in ISO 8601 format")
):
    top_services = find_top_services_with_weighted_score(session, start_date, end_date)
    print(top_services)
    if not top_services:
        raise HTTPException(status_code=404, detail="No services found for the specified date range.")

    response = [{"service_id": service.id, "title": service.title, "photo_url": service.photo_url} for service in top_services]
    return response