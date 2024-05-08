from sqlmodel import Session, select

from ..models.users import User


def select_all_users(session: Session):
    return session.exec(select(User)).all()


def find_user(session: Session, email):
    return session.exec(select(User).where(User.email == email)).first()


def update_user(session: Session, user):
    session.merge(user)
    session.commit()


def find_user_by_id(session: Session, user_id):
    return session.exec(select(User).where(User.id == user_id)).first()


def save_user(session: Session, user):
    session.add(user)
    session.commit()
    session.refresh(user)
