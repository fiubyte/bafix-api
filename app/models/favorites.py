from typing import Optional

from pydantic import BaseModel
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, Relationship


class Favorite(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("user_id", "service_id", name="user_service_favorite_unique"),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id"
    )
    service_id: Optional[int] = Field(
        default=None, foreign_key="service.id"
    )
    user: "User" = Relationship(back_populates="user_favorites")
    service: "Service" = Relationship(back_populates="favorites")


class FavoriteRead(BaseModel):
    user_id: int
    service_id: int
