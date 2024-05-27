from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..auth import auth_handler
from ..clients.geoapify import get_coordinates_from_address
from ..dependencies import UserDependency, get_session
from ..models.enums.roles import Role
from ..models.users import UserRead, UserInput, User, UserReject
from ..repositories.service_contact import find_service_contacts
from ..repositories.service_view import find_service_views
from ..repositories.user import find_user, find_user_by_id, is_document_number_available

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", status_code=200, response_model=UserRead, description='Get a User by ID')
def get_user(
        user_id: int,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    user = find_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    user = UserRead.from_orm(user)
    return user


@router.get("/", status_code=200, response_model=list[UserRead], description='Get users')
def get_users(
        user_ids: str = None,
        session: Session = Depends(get_session),
):
    if user_ids:
        user_ids = user_ids.split(',')
        users = [find_user_by_id(session, user_id) for user_id in user_ids]
        users = [UserRead.from_orm(user) for user in users if user]
    else:
        users = []
    return users


# Only the web users are registered from this endpoint. The mobile users are upserted from /auth/login
@router.post("/", status_code=201, response_model=UserRead, description='Register a new user')
def create_user(
        user: UserInput,
        session: Session = Depends(get_session),
):
    role_to_create = Role.PROVIDER.value
    user_found = find_user(session, user.email)
    if user_found:
        if role_to_create in user_found.roles:
            raise HTTPException(status_code=400, detail='Email is taken')
    user_to_upsert = user_found

    address_lat, address_long = get_coordinates_from_address(user.street, user.street_number)
    hashed_pwd = auth_handler.get_password_hash(user.password)
    if not user_to_upsert:
        # Insert: no previous user
        user_to_upsert = User(email=user.email, password=hashed_pwd, roles=role_to_create, name=user.name,
                              surname=user.surname, approved=None,
                              profile_photo_url=user.profile_photo_url, document_number=user.document_number,
                              document_photo_url=user.document_photo_url,
                              street=user.street, street_number=user.street_number, postal_code=user.postal_code,
                              address_lat=address_lat, address_long=address_long, max_radius=user.max_radius,
                              phone_number=user.phone_number)
    else:
        # Upsert: previous user created from mobile, merge the data
        user_to_upsert.roles = user_to_upsert.roles + ',' + role_to_create
        user_to_upsert.password = hashed_pwd
        user_to_upsert.name = user.name
        user_to_upsert.surname = user.surname
        user_to_upsert.approved = None
        user_to_upsert.profile_photo_url = user.profile_photo_url
        user_to_upsert.document_number = user.document_number
        user_to_upsert.document_photo_url = user.document_photo_url
        user_to_upsert.street = user.street
        user_to_upsert.street_number = user.street_number
        user_to_upsert.postal_code = user.postal_code
        user_to_upsert.address_lat = address_lat
        user_to_upsert.address_long = address_long
        user_to_upsert.max_radius = user.max_radius
        user_to_upsert.phone_number = user.phone_number

    session.add(user_to_upsert)
    session.commit()
    session.refresh(user_to_upsert)
    return user_to_upsert


@router.post("/{user_id}/approve", status_code=200, response_model=UserRead)
def approve_user(
        user_id: int,
        user: UserDependency,
        session: Session = Depends(get_session),
):
    user = find_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    user.approved = True
    user.rejected_message = ''
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/{user_id}/reject", status_code=200, response_model=UserRead)
def reject_user(
        user_id: int,
        user_reject: UserReject,
        user: UserDependency,
        session: Session = Depends(get_session),
):
    user = find_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    for service in user.services:
        service.approved = False
        service.rejected_message = user_reject.rejected_message

    user.approved = False
    user.rejected_message = user_reject.rejected_message
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/{user_id}/review", status_code=200, response_model=UserRead)
def put_user_to_review(
        user_id: int,
        user: UserDependency,
        session: Session = Depends(get_session),
):
    user = find_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    user.approved = None
    user.rejected_message = ''
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/document_available/{document_number}", description='Check if a document number is available')
def check_document_availability(document_number: str, session: Session = Depends(get_session)):
    is_available = is_document_number_available(document_number, session)
    return {"available": is_available}

@router.get("/{id}/views", status_code=200, description='Get views of a user')
def get_user_views(
        id: int,
        session: Session = Depends(get_session),
):
    user = find_user_by_id(session, id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    views = []
    for service in user.services:
        views += find_service_views(session, service.id)

    return views


@router.get("/{id}/contacts", status_code=200, description='Get contacts of a user')
def get_user_contacts(
        id: int,
        session: Session = Depends(get_session),
):
    user = find_user_by_id(session, id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    contacts = []
    for service in user.services:
        contacts += find_service_contacts(session, service.id)

    return contacts
