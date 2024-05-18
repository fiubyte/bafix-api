from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ServiceContactBase(SQLModel):
    pass


class ServiceContact(ServiceContactBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id"
    )
    service_id: Optional[int] = Field(
        default=None, foreign_key="service.id"
    )
    timestamp: datetime
