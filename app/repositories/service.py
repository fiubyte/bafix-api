from sqlmodel import Session, select

from .user import find_user_by_id
from ..dependencies import UserDependency
from ..models.favorites import Favorite
from ..models.rates import Rate, RateReadForFilter
from ..models.services import Service, User
from sqlalchemy import or_, and_, func, Float, cast, desc, asc, Table
import datetime
import pytz


def find_all_services(session: Session):
    return session.exec(select(Service)).all()


def find_services_for_user(session: Session, user_id: int):
    return session.exec(select(Service).where(Service.user_id == user_id)).all()


def find_service_by_id(session: Session, service_id: int):
    return session.exec(select(Service).where(Service.id == service_id)).first()


def save_service(session: Session, service: Service):
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


def get_actual_day(day_of_week):
    week_days = {
        "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miercoles",
        "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sabado",
        "Sunday": "Domingo"
    }
    return week_days.get(day_of_week, "")


def get_current_time_in_buenos_aires():
    timezone = pytz.timezone('America/Argentina/Buenos_Aires')
    now = datetime.datetime.now(timezone)
    return now


def get_filtered_services(user: UserDependency, session: Session, category_ids, user_ids, ordered_by_distance,
                          ordered_by_availability,
                          user_lat, user_long, roles, distance_filter, avaialability_filter, faved_only):
    now = get_current_time_in_buenos_aires()
    today = get_actual_day(now.strftime("%A"))
    current_time = now.time()
    user_lat = float(user_lat)
    user_long = float(user_long)

    distance_from_service = (
            6371 * func.acos(
        func.cos(func.radians(user_lat)) *
        func.cos(func.radians(cast(User.address_lat, Float))) *
        func.cos(func.radians(cast(User.address_long, Float)) - func.radians(user_long)) +
        func.sin(func.radians(user_lat)) *
        func.sin(func.radians(cast(User.address_lat, Float)))
    )
    )

    availability_condition = and_(
        Service.availability_days.contains(today),
        func.time(Service.availability_time_start) <= current_time,
        func.time(Service.availability_time_end) >= current_time
    )

    query = session.query(
        Service,
        User,
        distance_from_service.label('distance'),
        availability_condition.label('is_available')
    ).join(User, Service.user_id == User.id)

    if faved_only:
        query = query.join(Favorite, Service.id == Favorite.service_id)

    conditions = []

    if category_ids:
        conditions.append(Service.service_category_id.in_(category_ids))
    if user_ids:
        conditions.append(Service.user_id.in_(user_ids))
    if roles == "USER":
        conditions.append(Service.approved == True)
    if avaialability_filter:
        conditions.append(availability_condition)
    if faved_only:
        conditions.append(Favorite.user_id == user.id)

    conditions.append(distance_from_service <= distance_filter)

    if conditions:
        query = query.filter(*conditions)

    if ordered_by_distance and ordered_by_availability:
        query = query.order_by(desc(availability_condition.label('is_available')),
                               asc(distance_from_service.label('distance')))
    elif ordered_by_distance:
        query = query.order_by(asc(distance_from_service.label('distance')))
    elif ordered_by_availability:
        query = query.order_by(desc(availability_condition.label('is_available')))
    return query.all()


def find_average_rate_for_service(session: Session, service_id: int):
    avg_rate = session.query(func.avg(Rate.rate)).filter(Rate.service_id == service_id).filter(Rate.approved == True)
    if not avg_rate:
        return None
    return avg_rate.scalar()


def find_user_rate_for_service(session: Session, service_id: int, user_id: int):
    result = session.query(Rate).filter(Rate.service_id == service_id, Rate.user_id == user_id).first()
    return result if result else None


def find_user_rate_approved_for_service(session: Session, service_id: int, user_id: int):
    result = find_user_rate_for_service(session, service_id, user_id)
    return result.approved if result and result.approved else None


def find_user_rate_value_for_service(session: Session, service_id: int, user_id: int):
    result = find_user_rate_for_service(session, service_id, user_id)
    return result.rate if result else None


def find_rates_for_service(session: Session, service_id: int):
    found_rates = session.exec(select(Rate).where(Rate.service_id == service_id)).all()
    results = []
    if not found_rates:
        return results

    for rate in found_rates:
        user = find_user_by_id(session, rate.user_id)
        results.append(RateReadForFilter(
            message=rate.message, user_id=rate.user_id, service_id=rate.service_id,
            rate=rate.rate, name=user.name, surname=user.surname, profile_photo_url=user.profile_photo_url,
            approved=rate.approved))
    return results
