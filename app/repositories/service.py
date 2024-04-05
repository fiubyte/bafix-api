from sqlmodel import Session, select

from ..models.services import Service


def find_all(session: Session):
    return session.exec(select(Service)).all()
