from typing import Optional, Any

from pydantic import validator, BaseModel
from sqlmodel import Field, SQLModel, Relationship

from app.models.service_categories import ServiceCategory
from app.models.users import User, UserRead


class ServiceBase(SQLModel):
    service_category_id: Optional[int] = Field(default=None, foreign_key="servicecategory.id")
    title: str = "Service name"
    description: str = "Service description"
    photo_url: Optional[
        str] = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRS-GKiRj33HOaschW6KyQTivS2-IiwUvsYpCov-9AGgw&s"
    availability_time_start: str = "9:00"
    availability_time_end: str = "18:00"
    availability_days: str = "Lunes,Martes,Miercoles,Jueves,Viernes"

    # Important for PATCH /services
    @validator('*')
    def empty_str_to_none(cls, v):
        if v == '':
            return None
        return v


class Service(ServiceBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="services")
    approved: bool = None
    rejected_message: Optional[str]
    service_category: ServiceCategory = Relationship()


class ServiceCreate(ServiceBase):
    pass


class ServiceRead(ServiceBase):
    id: int
    user: UserRead
    service_category: ServiceCategory
    approved: Optional[bool]
    rejected_message: Optional[str]


class ServiceUpdate(ServiceBase):
    pass


class ServiceReject(SQLModel):
    rejected_message: Optional[str]


class ServiceResponseModel(BaseModel):
    id: int
    title: str
    description: str
    photo_url: str
    availability_time_start: str
    availability_time_end: str
    availability_days: str
    service_latitude: Optional[str] = None
    service_longitude: Optional[str] = None
    user_id: int
    user_name: str
    user_surname: str
    user_profile_photo_url: str
    user_phone_number: str
    distance: Optional[float] = None
    is_available: Optional[bool] = None

