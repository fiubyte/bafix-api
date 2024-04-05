from typing import Optional

from sqlmodel import Field, SQLModel, Relationship

from app.models.users import User


class ServiceBase(SQLModel):
    # Id is Optional because it is auto generated
    id: Optional[int] = Field(default=None, primary_key=True)
    approved: bool = False
    title: str = None
    description: str = None
    photo_url: Optional[str] = None
    availability_time_start: str = None
    availability_time_end: str = None
    availability_days: str = None


class Service(ServiceBase, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="services")
    service_category_id: Optional[int] = Field(default=None, foreign_key="servicecategory.id")
    pass


class ServiceCreate(ServiceBase):
    pass


class ServiceRead(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    pass
