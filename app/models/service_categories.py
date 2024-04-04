from typing import Optional

from sqlmodel import Field, SQLModel


class ServiceCategoriesBase(SQLModel):
    # Id is Optional because it is auto generated
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None


class ServiceCategories(ServiceCategoriesBase, table=True):
    # user_id
    # service_category_id
    pass
