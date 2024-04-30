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


class RateRead(BaseModel):
    message: str
    user_id: int
    service_id: int
    rate: int
    user_email: str
