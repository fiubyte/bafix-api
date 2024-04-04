from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..dependencies import UserDependency, get_session
from ..models.users import UserRead

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{id}", response_model=UserRead)
async def get_user(
        id: int,
        user: UserDependency,
        session: Session = Depends(get_session),
):
    services = []
    return services


@router.post("/", status_code=201)
async def create_user(
        user: UserDependency,
        session: Session = Depends(get_session)
):
    return None
