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
        roles=Role.ADMIN.value,
        name="admin",
        surname="admin",
        profile_photo_url="data:image/jpeg;base64,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",
        document_number="45201921",
        address="Av. Corrientes 1368",
        address_lat="-34.60408967755102",
        address_ong="-58.38604247551021",
        max_radius="2",
        phone_number="+5491140298321"
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
