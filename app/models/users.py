import datetime
from typing import Optional

from pydantic import validator, EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(index=True)
    roles: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    profile_photo_url: Optional[str] = None
    # google_id?
    document_number: Optional[str] = None
    address: Optional[str] = None
    address_lat: Optional[str] = None
    address_long: Optional[str] = None
    max_radius: Optional[int] = None
    phone_number: Optional[str] = None


class User(UserBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    password: str = Field(max_length=256, min_length=6)
    created_at: datetime.datetime = datetime.datetime.now()


class UserInput(SQLModel):
    username: str
    password: str = Field(max_length=256, min_length=6)
    password2: str
    email: EmailStr

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords don\'t match')
        return v


class UserLogin(SQLModel):
    username: str = "admin"
    password: str = "admin"


class UserUpdate(SQLModel):
    email: EmailStr = None


class UserRead(UserBase):
    id: int
    created_at: datetime.datetime
