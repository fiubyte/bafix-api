from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, Relationship

from pydantic import BaseModel


class RateBase(SQLModel):
    rate: Optional[int]
    message: Optional[str]


class Rate(RateBase, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "service_id", name="user_service_unique"),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id"
    )
    service_id: Optional[int] = Field(
        default=None, foreign_key="service.id"
    )
    user: "User" = Relationship(back_populates="user_rates")
    service: "Service" = Relationship(back_populates="rates")
    approved: Optional[bool]
    user_name: Optional[str]
    user_surname: Optional[str]
    user_email: Optional[str]


class RateRead(BaseModel):
    message: str
    user_id: int
    service_id: int
    rate: int
    user_email: str
    approved: Optional[bool]


class RateReadForFilter(BaseModel):
    message: str
    user_id: int
    service_id: int
    rate: int
    name: str
    surname: str
    profile_photo_url: str
    approved: Optional[bool]
