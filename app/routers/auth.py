from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..auth import auth_handler
from ..dependencies import get_session
from ..models.users import UserLogin
from ..repositories.user_repository import find_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=Any)
def login(user: UserLogin, session: Session = Depends(get_session)):
    user_found = find_user(session, user.email)
    if not user_found:
        raise HTTPException(status_code=401,
                            detail='Invalid email and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401,
                            detail='Invalid email and/or password')
    token = auth_handler.encode_token(user_found.email, user_found.roles)
    return {'token': token}
