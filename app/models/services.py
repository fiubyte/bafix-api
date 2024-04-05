from typing import Optional

from sqlmodel import Field, SQLModel, Relationship

from app.models.service_categories import ServiceCategory
from app.models.users import User, UserRead


class ServiceBase(SQLModel):
    service_category_id: Optional[int] = Field(default=None, foreign_key="servicecategory.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    approved: bool = False
    title: str = "Service name"
    description: str = "Service description"
    photo_url: Optional[str] = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRS-GKiRj33HOaschW6KyQTivS2-IiwUvsYpCov-9AGgw&s"
    availability_time_start: str = "9:00"
    availability_time_end: str = "18:00"
    availability_days: str = "Lunes,Martes,Miercoles,Jueves,Viernes"


class Service(ServiceBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates="services")
    service_category: ServiceCategory = Relationship()
    pass


class ServiceCreate(ServiceBase):
    pass


class ServiceRead(ServiceBase):
    id: int
    user: UserRead
    service_category: ServiceCategory


class ServiceUpdate(ServiceBase):
    pass
