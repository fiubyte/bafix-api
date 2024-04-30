from sqlmodel import Session, select

from app.models.rates import Rate


def save_rate(session: Session, rate: Rate):
    session.add(rate)
    session.commit()
    session.refresh(rate)
    return rate


def find_rate_by_id(session: Session, rate_id: int):
    return session.exec(select(Rate).where(Rate.id == rate_id)).first()

def find_rate_by_user_id_and_service_id(session: Session, user_id: int, service_id: int):
    return session.exec(select(Rate).where(Rate.user_id == user_id).where(Rate.service_id == service_id)).first()