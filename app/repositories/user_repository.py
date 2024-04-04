from sqlmodel import Session, select

from ..models.users import User


def select_all_users(session: Session):
    return session.exec(select(User)).all()


def find_user(session: Session, name):
    return session.exec(select(User).where(User.username == name)).first()


def update_user(session: Session, user):
    session.merge(user)
    session.commit()
