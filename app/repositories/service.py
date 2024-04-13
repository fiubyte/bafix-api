from sqlmodel import Session, select

from ..models.service_categories import ServiceCategory
from ..models.services import Service, User
from sqlalchemy import or_, and_, func, Float, cast


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


def get_filtered_services(session: Session, category_ids, user_ids, days, distance, user_lat, user_long, check_time,
                          roles):
    distance_expression = (
            6371 * func.acos(
        func.cos(func.radians(user_lat)) *
        func.cos(func.radians(User.address_lat)) *
        func.cos(func.radians(User.address_long) - func.radians(user_long)) +
        func.sin(func.radians(user_lat)) *
        func.sin(func.radians(User.address_lat))
    )
    )

    query = session.query(
        Service,
        ServiceCategory,
        User,
        distance_expression.label('distance')
    ).join(User, Service.user_id == User.id).join(ServiceCategory, ServiceCategory.id == Service.service_category_id)

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
    if roles == "USER":
        conditions.append(Service.approved == True)

    # distance_filter = (
    # func.acos(
    #     func.sin(func.radians(cast(User.address_lat, Float))) * func.sin(func.radians(user_lat)) +
    #     func.cos(func.radians(cast(User.address_lat, Float))) * func.cos(func.radians(user_lat)) *
    #     func.cos(func.radians(cast(User.address_long, Float) - user_long))
    # ) * 6371 <= distance)    

    # query = query.filter(distance_filter)
    if conditions:
        query = query.filter(*conditions)

    query = query.order_by('distance')
    return query.all()
