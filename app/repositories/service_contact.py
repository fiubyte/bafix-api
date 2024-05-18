from sqlmodel import Session

from app.models.service_contact import ServiceContact


def save_service_contact(session: Session, service_contact: ServiceContact):
    session.add(service_contact)
    session.commit()
    session.refresh(service_contact)
    return service_contact


def find_service_contacts(session: Session, service_id: int):
    result = session.query(ServiceContact).filter(ServiceContact.service_id == service_id).all()
    return result if result else None
