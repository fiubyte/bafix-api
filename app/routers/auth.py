from typing import Any

from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..dependencies import UserDependency, get_session

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=Any)
async def login(
        user: UserDependency,
        session: Session = Depends(get_session)
):
    return None
