from sqlmodel import Session, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, and_, cast
from sqlalchemy.types import Float
from sqlalchemy import or_
from sqlalchemy.sql.expression import select
from ..models.services import Service
from ..models.users import User


def find_all(session: Session):
    return session.exec(select(Service)).all()


def find_services_for_user(session: Session, user_id: int):
    return session.exec(select(Service).where(Service.user_id == user_id)).all()


def find_service_by_id(session: Session, service_id: int):
    return session.exec(select(Service).where(Service.id == service_id)).first()


def get_filtered_services(session: Session, category_ids, user_ids, days, distance, user_lat, user_long, check_time):
    query = session.query(
        Service, 
        User.name, 
        User.email, 
        User.address,  
        User.address_lat, 
        User.address_long,
        User.approved 
    ).join(User, Service.user_id == User.id)

    conditions = []

    if category_ids:
        conditions.append(Service.service_category_id.in_(category_ids))
    if user_ids:
        conditions.append(Service.user_id.in_(user_ids))
    if days:
        day_conditions = [Service.availability_days.contains(day) for day in days]
        conditions.append(or_(*day_conditions))
    
    if check_time:
        conditions.append(and_(
            Service.availability_time_start <= check_time,
            Service.availability_time_end >= check_time
    ))
    

    distance_filter = (
    func.acos(
        func.sin(func.radians(cast(User.address_lat, Float))) * func.sin(func.radians(user_lat)) +
        func.cos(func.radians(cast(User.address_lat, Float))) * func.cos(func.radians(user_lat)) *
        func.cos(func.radians(cast(User.address_long, Float) - user_long))
    ) * 6371 <= distance)    

    query = query.filter(distance_filter)
    if conditions:
        query = query.filter(*conditions)

    return query.all()