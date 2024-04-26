from sqlmodel import Session, select

from app.models.rates import Rate


def save_rate(session: Session, rate: Rate):
    session.add(rate)
    session.commit()
    session.refresh(rate)
    return rate


def find_rate_by_id(session: Session, rate_id: int):
    return session.exec(select(Rate).where(Rate.id == rate_id)).first()
