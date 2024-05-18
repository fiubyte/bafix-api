import datetime
from typing import Optional

from pydantic import validator, EmailStr
from sqlmodel import Field, SQLModel, Relationship

from app.models.enums.roles import Role


class UserBase(SQLModel):
    email: EmailStr = Field(index=True)
    name: Optional[str] = ""
    surname: Optional[str] = ""
    profile_photo_url: Optional[str] = ""
    document_number: Optional[str] = ""
    document_photo_url: Optional[str] = ""
    street: Optional[str] = ""
    street_number: Optional[str] = ""
    postal_code: Optional[str] = ""
    max_radius: Optional[float] = 0.0
    phone_number: Optional[str] = ""


class User(UserBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    password: Optional[str] = Field(max_length=256, min_length=5)
    created_at: datetime.datetime = datetime.datetime.now()
    approved: Optional[bool] = None
    rejected_message: Optional[str]
    roles: Optional[str] = Role.USER.value + ',' + Role.PROVIDER.value
    services: list["Service"] = Relationship(back_populates="user")
    user_rates: Optional[list["Rate"]] = Relationship(back_populates="user")
    user_favorites: Optional[list["Favorite"]] = Relationship(back_populates="user")
    address_lat: Optional[str] = ""
    address_long: Optional[str] = ""


class UserRead(UserBase):
    id: int
    created_at: datetime.datetime
    approved: Optional[bool]
    rejected_message: Optional[str]
    services: list
    address_lat: Optional[str]
    address_long: Optional[str]


class UserInput(UserBase):
    password: Optional[str] = Field(max_length=256, min_length=6)
    password2: Optional[str]

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords don\'t match')
        return v


class UserLogin(SQLModel):
    email: str = "admin@example.com"
    password: str = "admin"
    fullName: Optional[str]
    google_id_token: Optional[str]


class UserUpdate(SQLModel):
    email: EmailStr = None


class UserReject(SQLModel):
    rejected_message: Optional[str]
