from typing import Optional

from sqlmodel import Field, SQLModel


class ServiceBase(SQLModel):
    # Id is Optional because it is auto generated
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    approval_status: str = None
    title: str = None
    description: str = None
    photo_url: Optional[str] = None
    availability_time_start: str = None
    availability_time_end: str = None
    availability_days: str = None


class Service(ServiceBase, table=True):
    # user_id
    # service_category_id
    pass


class ServiceCreate(ServiceBase):
    pass


class ServiceRead(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    pass
