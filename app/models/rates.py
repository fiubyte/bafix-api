from typing import Optional

from sqlmodel import Field, SQLModel, Relationship


class RateBase(SQLModel):
    rate: Optional[int]
    message: Optional[str]


class Rate(RateBase, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    service_id: Optional[int] = Field(
        default=None, foreign_key="service.id", primary_key=True
    )
    user: "User" = Relationship(back_populates="user_rates")
    service: "Service" = Relationship(back_populates="rates")


class RateRead(RateBase):
    pass
