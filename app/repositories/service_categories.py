from sqlmodel import Session, select

from ..models.service_categories import ServiceCategory


def find_all_service_categories(session: Session):
    return session.exec(select(ServiceCategory)).all()
