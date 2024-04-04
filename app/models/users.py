import datetime
from typing import Optional

from pydantic import validator, EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email: EmailStr = Field(index=True)
    roles: Optional[str] = "USER,PROVIDER"
    name: Optional[str] = "John"
    surname: Optional[str] = "Doe"
    profile_photo_url: Optional[str] = "https://www.cronista.com/files/image/401/401221/618bebe24727e.jpg"
    # google_id?
    document_number: Optional[str] = "40123456"
    address: Optional[str] = "Av. Corrientes 1368"
    address_lat: Optional[str] = "-34.604110"
    address_long: Optional[str] = "-58.386020"
    max_radius: Optional[int] = "1"
    phone_number: Optional[str] = "+5491142022983"


class User(UserBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    password: str = Field(max_length=256, min_length=6)
    created_at: datetime.datetime = datetime.datetime.now()


class UserInput(UserBase):
    password: str = Field(max_length=256, min_length=6)
    password2: str

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords don\'t match')
        return v


class UserLogin(SQLModel):
    email: str = "admin@example.com"
    password: str = "admin"


class UserUpdate(SQLModel):
    email: EmailStr = None


class UserRead(UserBase):
    id: int
    created_at: datetime.datetime
