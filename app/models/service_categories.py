from typing import Optional

from sqlmodel import Field, SQLModel


class ServiceCategoryBase(SQLModel):
    # Id is Optional because it is auto generated
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None


class ServiceCategory(ServiceCategoryBase, table=True):
    # user_id
    # service_category_id
    pass
