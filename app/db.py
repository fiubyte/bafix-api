import os

from sqlmodel import SQLModel, create_engine, Session

from .auth import auth_handler
from .models.service_categories import ServiceCategory
from .models.services import Service
from .models.users import User

db_url = "postgresql://{}:{}@{}:{}/{}".format(
    "bafix", os.environ['DB_PASSWORD'], "dpg-cnug04acn0vc73b6mrrg-a.oregon-postgres.render.com", 5432, "bafix_db"
)
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def drop_db():
    SQLModel.metadata.drop_all(engine)


users = [
    User(
        id=1,
        email="admin@example.com",
        password=auth_handler.get_password_hash("admin"),
        roles="ADMIN"
    )
]

service_categories = [
    ServiceCategory(
        id=1,
        title="Plomería",
        description="Servicios de plomería en general",
    ),
    ServiceCategory(
        id=2,
        title="Electricista",
        description="Servicios de electricista en general",
    )
]

services = [
    Service(
        user_id=1,
        service_category_id=1,
        approved=True,
        title="Reparación de cañerías y destapaciones",
        description="Servicios de cañerías, destapaciones, plomería en general",
        photo_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRS-GKiRj33HOaschW6KyQTivS2-IiwUvsYpCov-9AGgw&s",
        availability_time_start="9:00",
        availability_time_end="19:00",
        availability_days="Lunes,Martes,Miercoles,Jueves,Viernes"
    )
]


def seed_db():
    with Session(engine) as session:
        for user in users:
            session.add(user)
        session.commit()

        for service_category in service_categories:
            session.add(service_category)
        session.commit()

        for service in services:
            session.add(service)
        session.commit()
