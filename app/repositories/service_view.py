from sqlmodel import Session

from app.models.service_view import ServiceView


def save_service_view(session: Session, service_view: ServiceView):
    session.add(service_view)
    session.commit()
    session.refresh(service_view)
    return service_view


def find_service_views(session: Session, service_id: int):
    result = session.query(ServiceView).filter(ServiceView.service_id == service_id).all()
    return result if result else None
