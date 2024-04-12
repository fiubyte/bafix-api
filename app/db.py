import os

from sqlmodel import SQLModel, create_engine, Session

from .auth import auth_handler
from .models.enums.roles import Role
from .models.service_categories import ServiceCategory
from .models.services import Service
from .models.users import User

if os.getenv('ENV', 'local') == 'local':
    # Local disk database
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
    print("Connected to local BA Fix DB")
else:
    db_url = "postgresql://{}:{}@{}:{}/{}".format(
        "bafix", os.environ['DB_PASSWORD'], "dpg-coc6svgl5elc739ob64g-a.oregon-postgres.render.com", 5432, "bafix_db_9tkt"
    )
    engine = create_engine(db_url, echo=True)
    print("Connected to remote BA Fix DB")


def init_db():
    SQLModel.metadata.create_all(engine)


def drop_db():
    SQLModel.metadata.drop_all(engine)


users = [
    User(
        email="admin@example.com",
        password=auth_handler.get_password_hash("admin"),
        roles=Role.ADMIN.value,
        approved=True,
        name="admin",
        surname="admin",
        profile_photo_url="https://blogs.unitec.mx/hubfs/287524/Imported_Blog_Media/diferencias-entre-un-jefe-y-un-lider-00-Dec-17-2022-09-00-11-1661-PM.jpg",
        document_number="45201921",
        street="Av. Corrientes",
        street_number="1368",
        address_lat="-34.60408967755102",
        address_long="-58.38604247551021",
        postal_code='1416',
        max_radius="2",
        phone_number="+5491140298321"
    ),
    User(
        email="jbenavidez@gmail.com",
        password=auth_handler.get_password_hash("jbenavidez"),
        roles=Role.USER.value,
        approved=True,
        name="Julia",
        surname="Benavídez",
        profile_photo_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0Iic5z8QzT-nApNASwkzBwysnrgOPol2TrKSmQuzFMQ&s",
        document_number="17558441",
        street="Jeronimo Salguero",
        street_number="152",
        address_lat="-34.609215881245625",
        address_long="-58.420097140506904",
        postal_code='1177',
        max_radius="0.8",
        phone_number="+5491132528746"
    ),
    User(
        email="mdelgado@gmail.com",
        password=auth_handler.get_password_hash("mdelgadp"),
        roles=Role.USER.value,
        approved=True,
        name="Mario",
        surname="Delgado",
        profile_photo_url="https://media.licdn.com/dms/image/D5603AQHLbg5rTqWVxg/profile-displayphoto-shrink_800_800/0/1701358765677?e=2147483647&v=beta&t=6cWa7LwVmv9IXXJGLgVVznLKHk7UpFkPyzukxBFgreY",
        document_number="18255477",
        street="Av. Rivadavia",
        street_number="1147",
        address_lat="-34.60840982966",
        address_long="-58.38257618714883",
        postal_code='1033',
        max_radius="2.5",
        phone_number="+5491145786596"
    ),
    User(
        email="amolina@gmail.com",
        password=auth_handler.get_password_hash("amolina"),
        roles=Role.USER.value,
        approved=True,
        name="Augusto",
        surname="Molina",
        profile_photo_url="https://media.licdn.com/dms/image/C4E03AQFebLf0pN9Zng/profile-displayphoto-shrink_200_200/0/1583265319814?e=2147483647&v=beta&t=N432_9aBMwV2DsrVzNoECCc2xXDclrR5b2jACyt_l7M",
        document_number="14758693",
        street="Av. Las Heras",
        street_number="2457",
        address_lat="-34.58594398110941",
        address_long="-58.398505915985815",
        postal_code='1425',
        max_radius="11",
        phone_number="+5491114562258"
    ),
    User(
        email="nperez@gmail.com",
        password=auth_handler.get_password_hash("nperez"),
        roles=Role.USER.value,
        approved=True,
        name="Nadia",
        surname="Perez",
        profile_photo_url="https://media.licdn.com/dms/image/D4D03AQEW4x_hKWsXCw/profile-displayphoto-shrink_800_800/0/1679593696220?e=2147483647&v=beta&t=2fyjlrCniINcZDLkO1Tucv_ca3f2RRjMfmgQi05L0pU",
        document_number="38554211",
        street="Arias",
        street_number="1225",
        address_lat="-34.54519480487854",
        address_long="-58.48203388715096",
        postal_code='1429',
        max_radius="1",
        phone_number="+5491174485662"
    ),
        User(
        email="cpasaft@gmail.com",
        password=auth_handler.get_password_hash("cpasaft"),
        roles=Role.USER.value,
        approved=True,
        name="Carla",
        surname="Pasaft",
        profile_photo_url="https://media.licdn.com/dms/image/C4D03AQE4TZGcd3n8cg/profile-displayphoto-shrink_800_800/0/1659910226226?e=2147483647&v=beta&t=FSW0P77J2QbKhdVF1xD-ebOZJdqQ-954pxRBob-AJhs",
        document_number="28544121",
        street="Salom",
        street_number="337",
        address_lat="-34.6464564623936",
        address_long="-58.38277346103068",
        postal_code='1277',
        max_radius="2.5",
        phone_number="+5491124546856"
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
    ),
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
