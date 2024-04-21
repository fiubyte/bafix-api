from sqlmodel import Session

from app.models.rates import Rate


def save_rate(session: Session, rate: Rate):
    session.add(rate)
    session.commit()
    session.refresh(rate)
    return rate
