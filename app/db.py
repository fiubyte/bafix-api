import os

from sqlmodel import SQLModel, create_engine, Session

from .auth import auth_handler
from .models.enums.roles import Role
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
        roles=Role.ADMIN.value
    )
]

service_categories = [
    ServiceCategory(
        title="Plomería",
        description="Servicios de plomería",
    ),
    ServiceCategory(
        title="Pinturería",
        description="Servicios de pintura",
    ),
    ServiceCategory(
        title="Albañilería",
        description="Servicios de albañilería",
    ),
    ServiceCategory(
        title="Carpintería",
        description="Servicios de carpintería",
    ),
    ServiceCategory(
        title="Gasista",
        description="Servicios de gas",
    ),
    ServiceCategory(
        title="Mecánico",
        description="Servicios de mecánica",
    ),
    ServiceCategory(
        title="Electricista",
        description="Servicios de electricidad",
    ),
    ServiceCategory(
        title="Cerrajería",
        description="Servicios de cerrajería",
    ),
    ServiceCategory(
        title="Reparación de electrodomésticos",
        description="Servicios de reparación de electrodomésticos",
    ),
    ServiceCategory(
        title="Instalación de aires acondicionados",
        description="Servicios de instalación de aires acondicionados",
    ),
    ServiceCategory(
        title="Jardinería/Paisajista",
        description="Servicios de jardinería y paisajismo",
    ),
    ServiceCategory(
        title="Decoración de interiores",
        description="Servicios de decoración de interiores",
    ),
    ServiceCategory(
        title="Arquitectura",
        description="Servicios de arquitectura",
    ),
    ServiceCategory(
        title="Pedicuría/Manicuría",
        description="Servicios de pedicura y manicura",
    ),
    ServiceCategory(
        title="Peluquería",
        description="Servicios de peluquería",
    ),
    ServiceCategory(
        title="Abogados",
        description="Servicios de abogado",
    ),
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
