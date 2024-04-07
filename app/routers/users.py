from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session
from user_agents import parse

from ..auth import auth_handler
from ..dependencies import UserDependency, get_session
from ..models.enums.roles import Role
from ..models.users import UserRead, UserInput, User
from ..repositories.user_repository import select_all_users, find_user, find_user_by_id

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}", response_model=UserRead, description='Get a User by ID')
def get_user(
        user_id: int,
        user: UserDependency,
        session: Session = Depends(get_session)
):
    user = find_user_by_id(session, user_id)
    user = UserRead.from_orm(user)
    return user


@router.post("/", status_code=201, response_model=UserRead, description='Register a new user')
def create_user(
        user: UserInput,
        session: Session = Depends(get_session),
        user_agent: Annotated[Union[str, None], Header()] = None
):
    user_agent_parsed = parse(user_agent)
    role_to_create = Role.PROVIDER.value
    if user_agent_parsed.is_mobile:
        role_to_create = Role.USER.value

    users = select_all_users(session)
    user_to_upsert = None

    for u in users:
        if u.email == user.email:
            if role_to_create in u.roles:
                raise HTTPException(status_code=400, detail='Email is taken')
            user_to_upsert = u

    hashed_pwd = auth_handler.get_password_hash(user.password)
    if not user_to_upsert:
        # Insert: no previous user
        user_to_upsert = User(email=user.email, password=hashed_pwd, roles=role_to_create, name=user.name,
                              surname=user.surname,
                              profile_photo_url=user.profile_photo_url, document_number=user.document_number,
                              address=user.address,
                              address_lat=user.address_lat, address_long=user.address_long, max_radius=user.max_radius,
                              phone_number=user.phone_number)
    else:
        # Upsert: previous user, merge the data
        user_to_upsert.roles = user_to_upsert.roles + ',' + role_to_create
        # TODO: google login fields

    session.add(user_to_upsert)
    session.commit()
    session.refresh(user_to_upsert)
    return user_to_upsert
