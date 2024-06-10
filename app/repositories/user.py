import itertools
from datetime import datetime

from sqlalchemy import func
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


def is_document_number_available(document_number: str, session: Session):
    document = session.exec(select(User).where(User.document_number == document_number)).first()
    return document is None


def find_total_users(session: Session, start: datetime, end: datetime, role: str):
    query_all_users = session.query(User).filter(User.created_at >= start).filter(User.created_at <= end)
    if role:
        query_all_users = query_all_users.filter(User.roles.like(f'%{role}%'))

    result = (query_all_users.all())

    query_previous_users = session.query(func.count(User.id)).filter(User.created_at < start)
    if role:
        query_previous_users = query_previous_users.filter(User.roles.like(f'%{role}%'))

    total_users_previous_to_start_date = (query_previous_users.all())[0][0]

    def grouper(user):
        return user.created_at.year, user.created_at.month, user.created_at.day

    date_format = '%Y-%m-%d'

    response = {}
    for ((year, month, day), items) in itertools.groupby(result, grouper):
        if not datetime.strptime("%s-%s-%s" % (year, month, day), date_format) in response:
            response[datetime.strptime("%s-%s-%s" % (year, month, day), date_format)] = 0
        for _ in items:
            response[datetime.strptime("%s-%s-%s" % (year, month, day), date_format)] = response[datetime.strptime(
                "%s-%s-%s" % (year, month, day), date_format)] + 1
    response = dict(sorted(response.items()))
    previous_total_users = total_users_previous_to_start_date
    for key, value in response.items():
        response[key] = response[key] + previous_total_users
        previous_total_users = response[key]

    return response if response else None
