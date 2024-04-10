from sqlmodel import Session, select

from ..models.services import Service


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
