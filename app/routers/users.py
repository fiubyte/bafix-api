from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..auth import auth_handler
from ..dependencies import UserDependency, get_session
from ..models.users import UserRead, UserInput, User
from ..repositories.user_repository import select_all_users

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}", response_model=UserRead, description='Get a User by ID')
async def get_user(
        id: int,
        user: UserDependency,
        session: Session = Depends(get_session),
):
    services = []
    return services


@router.post("/", status_code=201, response_model=User, description='Register a new user')
def create_user(
        user: UserInput,
        session: Session = Depends(get_session)
):
    users = select_all_users(session)
    if any(x.email == user.email for x in users):
        raise HTTPException(status_code=400, detail='Email is taken')

    hashed_pwd = auth_handler.get_password_hash(user.password)
    u = User(email=user.email, password=hashed_pwd, roles=user.roles, name=user.name, surname=user.surname,
             profile_photo_url=user.profile_photo_url, document_number=user.document_number, address=user.address,
             address_lat=user.address_lat, address_long=user.address_long, max_radius=user.max_radius,
             phone_number=user.phone_number)
    session.add(u)
    session.commit()
    session.refresh(u)
    return u
