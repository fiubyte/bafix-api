from sqlmodel import Session, select

from ..models.services import Service


def find_all(session: Session):
    return session.exec(select(Service)).all()


def find_service_by_id(session: Session, service_id: int):
    return session.exec(select(Service).where(Service.id == service_id)).first()
