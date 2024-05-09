from sqlmodel import Session, select

from app.models.favorites import Favorite


def save_favorite(session: Session, favorite: Favorite):
    session.add(favorite)
    session.commit()
    session.refresh(favorite)
    return favorite


def delete_favorite(session: Session, favorite: Favorite):
    session.delete(favorite)
    session.commit()


def find_favorite_by_user_id_and_service_id(session: Session, user_id: int, service_id: int):
    return session.exec(
        select(Favorite).where(Favorite.user_id == user_id).where(Favorite.service_id == service_id)).first()


def is_service_faved_by_user(session: Session, service_id: int, user_id: int):
    result = session.exec(
        select(Favorite).where(Favorite.user_id == user_id).where(Favorite.service_id == service_id)).first()
    if result:
        return True
    return False

