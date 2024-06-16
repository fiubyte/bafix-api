from sqlmodel import Session, select

from .user import find_user_by_id
from ..dependencies import UserDependency
from ..models.favorites import Favorite
from ..models.rates import Rate, RateReadForFilter
from ..models.service_contact import ServiceContact
from ..models.service_contact import ServiceContact
from ..models.service_view import ServiceView
from ..models.services import Service, User
from sqlalchemy import or_, and_, func, Float, cast, desc, asc, Table
import datetime
import pytz
import math


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
        # print(f"User username: {user.name}")
        results.append(rate)
    return results


def find_top_services_with_weighted_score(session: Session, start_date: datetime, end_date: datetime):
    subquery = (
        session.query(
            Service.id,
            func.avg(Rate.rate).label('average_rate'),
            func.count(ServiceContact.id).label('contact_count')
        )
        .join(Rate, Service.id == Rate.service_id)
        .join(ServiceContact, Service.id == ServiceContact.service_id)
        .filter(ServiceContact.timestamp.between(start_date, end_date))
        .group_by(Service.id)
        .subquery()
    )

    query = (
        session.query(
            Service.id,
            Service.title,
            Service.photo_url,
            (subquery.c.average_rate * 0.7 + subquery.c.contact_count * 0.3).label('weighted_score')
        )
        .join(subquery, Service.id == subquery.c.id)
        .order_by((subquery.c.average_rate * 0.7 + subquery.c.contact_count * 0.3).desc())
        .limit(5)
    )

    return session.execute(query).all()


def calculate_services_conversion_rate(session: Session, start: datetime, end: datetime):
    all_service_views = (session.query(Service)
                         .distinct(Service.id)
                         .all())

    result = {}
    for service in all_service_views:
        total_views = (session.query(func.count(ServiceView.id))
                       .where(ServiceView.service_id == service.id)
                       .filter(ServiceView.timestamp >= start)
                       .filter(ServiceView.timestamp <= end)
                       .all())[0][0]
        total_contacts = (session.query(func.count(ServiceContact.id))
                          .where(ServiceContact.service_id == service.id)
                          .filter(ServiceContact.timestamp >= start)
                          .filter(ServiceContact.timestamp <= end)
                          .all())[0][0]
        if total_views != 0:
            # result[service.id] = {"service_id": service.id, "title": service.title, "conversion_rate": (total_contacts / total_views) * 100}
            # result[service.id] = {"service_id": service.id, "title": service.title, "conversion_rate": (total_contacts / total_views) * math.log10(total_contacts + 1) * 100}
            result[service.id] = {"service_id": service.id, "title": service.title, "conversion_rate": (((total_contacts / total_views) * math.sqrt(total_views))/(math.sqrt(total_views) + 1)) * 100}

    # Efectividad = (Ventas / Contactos) x log (contactos +1)

    return {k: v for k, v in
            sorted(result.items(), key=lambda item: item[1]['conversion_rate'], reverse=True)} if result else None
