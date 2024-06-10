import datetime
from sqlmodel import Session
from sqlalchemy import func

from app.models.service_contact import ServiceContact


def save_service_contact(session: Session, service_contact: ServiceContact):
    session.add(service_contact)
    session.commit()
    session.refresh(service_contact)
    return service_contact


def find_service_contacts(session: Session, service_id: int):
    result = session.query(ServiceContact).filter(ServiceContact.service_id == service_id).all()
    return result if result else None

def find_top_contacts_users(session: Session, start: datetime, end: datetime):

    result = (session.query(ServiceContact.user_id, func.count(ServiceContact.user_id))
              .group_by(ServiceContact.user_id)
              .order_by(func.count(ServiceContact.user_id).desc())
              .filter(ServiceContact.timestamp >= start)
              .filter(ServiceContact.timestamp <= end)
              .limit(5))
    
    return result if result else None