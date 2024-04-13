import json
import os
from typing import Any

import firebase_admin
from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import auth, credentials
from sqlmodel import Session

from ..auth import auth_handler
from ..dependencies import get_session
from ..models.enums.roles import Role
from ..models.users import UserLogin, User
from ..repositories.user_repository import find_user, save_user, update_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

# Requires the env variable GOOGLE_APPLICATION_CREDENTIALS. See: https://firebase.google.com/docs/admin/setup
firebase_credentials = credentials.Certificate('/code/app/ba-fix-firebase-adminsdk.json')
bafix_firebase_app = firebase_admin.initialize_app(firebase_credentials)

@router.post("/login", response_model=Any)
def login(user: UserLogin, session: Session = Depends(get_session)):
    user_found = find_user(session, user.email)
    if not user.google_id_token:
        if not user_found:
            raise HTTPException(status_code=401,
                                detail='Invalid email and/or password')
        verified = auth_handler.verify_password(user.password, user_found.password)
        if not verified:
            raise HTTPException(status_code=401,
                                detail='Invalid email and/or password')
        token = auth_handler.encode_token(user_found.email, user_found.roles)
        return {'token': token}
    else:
        # Google/Firebase auth
        print('Attempting to verify google id token')
        decoded_token = auth.verify_id_token(user.google_id_token)
        print('Google id token verified successfully')
        # decoded_token['uid']
        # From this point on we confirm it's authenticated
        user_to_upsert = user_found
        if not user_to_upsert:
            user_to_upsert = User(email=user.email, roles=Role.USER.value)
            save_user(session, user_to_upsert)
        else:
            if not Role.USER.value in user_to_upsert.roles:
                user_to_upsert.roles = user_to_upsert.roles.append(',' + Role.USER.value)
                update_user(session, user_to_upsert)
        token = auth_handler.encode_token(user_to_upsert.email, user_to_upsert.roles)
        return {'token': token}
