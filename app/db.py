import os

from sqlmodel import SQLModel, create_engine, Session

from .auth import auth_handler
from .models.enums.roles import Role
from .models.favorites import Favorite
from .models.rates import Rate
from .models.service_categories import ServiceCategory
from .models.services import Service
from .models.users import User

if os.getenv('ENV', 'local') == 'local':
    # Local disk database
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)
    print("Connected to local BA Fix DB")
else:
    db_url = "postgresql://{}:{}@{}:{}/{}".format(
        "bafix", os.environ['DB_PASSWORD'], "dpg-coc6svgl5elc739ob64g-a.oregon-postgres.render.com", 5432,
        "bafix_db_9tkt"
    )
    engine = create_engine(db_url, echo=True)
    print("Connected to remote BA Fix DB")


def init_db():
    SQLModel.metadata.create_all(engine)


def drop_db():
    SQLModel.metadata.drop_all(engine)


user_admin = User(
    email="admin@example.com",
    password=auth_handler.get_password_hash("admin"),
    roles=Role.ADMIN.value,
    approved=True,
    name="admin",
    surname="admin",
    profile_photo_url="https://blogs.unitec.mx/hubfs/287524/Imported_Blog_Media/diferencias-entre-un-jefe-y-un-lider-00-Dec-17-2022-09-00-11-1661-PM.jpg",
    document_photo_url="https://tics.unaj.edu.ar/wp-content/uploads/sites/45/2021/03/Untitled-1-300x177.png",
    document_number="45201921",
    street="Av. Corrientes",
    street_number="1368",
    address_lat="-34.60408967755102",
    address_long="-58.38604247551021",
    postal_code='1416',
    max_radius=10.0,
    phone_number="+5491132637625"
)
user_1 = User(
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
    max_radius=10.0,
    phone_number="+5491132637625"
)
user_2 = User(
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
    max_radius=10,
    phone_number="+5491140922989"
)
user_3 = User(
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
    max_radius=50,
    phone_number="+5491156160047"
)
provider_1 = User(
    email="nperez@gmail.com",
    password=auth_handler.get_password_hash("nperez"),
    roles=Role.PROVIDER.value,
    approved=None,
    rejected_message="El documento ingresado no es válido en Argentina",
    name="Nadia",
    surname="Pérez",
    profile_photo_url="https://media.licdn.com/dms/image/D4D03AQEW4x_hKWsXCw/profile-displayphoto-shrink_800_800/0/1679593696220?e=2147483647&v=beta&t=2fyjlrCniINcZDLkO1Tucv_ca3f2RRjMfmgQi05L0pU",
    document_photo_url="https://tics.unaj.edu.ar/wp-content/uploads/sites/45/2021/03/Untitled-1-300x177.png",
    document_number="38554211",
    street="Arias",
    street_number="1225",
    address_lat="-34.54519480487854",
    address_long="-58.48203388715096",
    postal_code='1429',
    max_radius=1,
    phone_number="+5491132637625"
)
provider_2 = User(
    email="cpasaft@gmail.com",
    password=auth_handler.get_password_hash("cpasaft"),
    roles=Role.PROVIDER.value,
    approved=True,
    name="Carla",
    surname="Pasaft",
    profile_photo_url="https://media.licdn.com/dms/image/C4D03AQE4TZGcd3n8cg/profile-displayphoto-shrink_800_800/0/1659910226226?e=2147483647&v=beta&t=FSW0P77J2QbKhdVF1xD-ebOZJdqQ-954pxRBob-AJhs",
    document_photo_url="https://tics.unaj.edu.ar/wp-content/uploads/sites/45/2021/03/Untitled-1-300x177.png",
    document_number="28544121",
    street="Salom",
    street_number="337",
    address_lat="-34.6464564623936",
    address_long="-58.38277346103068",
    postal_code='1277',
    max_radius=2.5,
    phone_number="+358405550171"
)

provider_3 = User(
    email="tbotalla@hotmail.com",
    password=auth_handler.get_password_hash("tbotalla"),
    roles=Role.PROVIDER.value,
    approved=True,
    name="Tomas",
    surname="Botalla",
    profile_photo_url="https://www.shutterstock.com/image-photo/profile-picture-smiling-young-african-260nw-1873784920.jpg",
    document_photo_url="https://tics.unaj.edu.ar/wp-content/uploads/sites/45/2021/03/Untitled-1-300x177.png",
    document_number="25216293",
    street="Av. Cordoba",
    street_number="4326",
    address_lat="-34.6464564623936",
    address_long="-58.38277346103068",
    postal_code='1414',
    max_radius=2.5,
    phone_number="+5491140922989"
)

provider_4 = User(
    email="jramirez@hotmail.com",
    password=auth_handler.get_password_hash("tbotalla"),
    roles=Role.PROVIDER.value,
    approved=None,
    name="Juan",
    surname="Ramirez",
    profile_photo_url="https://www.shutterstock.com/image-photo/profile-picture-smiling-young-african-260nw-1873784920.jpg",
    document_photo_url="https://tics.unaj.edu.ar/wp-content/uploads/sites/45/2021/03/Untitled-1-300x177.png",
    document_number="25216293",
    street="Av. Cordoba",
    street_number="4326",
    address_lat="-34.6464564623936",
    address_long="-58.38277346103068",
    postal_code='1414',
    max_radius=2.5,
    phone_number="+5491156160047"
)

users = [
    user_admin,
    user_1,
    user_2,
    user_3,
    provider_1,
    provider_2,
    provider_3,
    provider_4
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
        title="Gasista",
        description="Servicios de gas",
    ),
    ServiceCategory(
        title="Carpintería",
        description="Servicios de carpintería",
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
        title="Reparación de electrodomésticos",
        description="Servicios de reparación de electrodomésticos",
    ),
    ServiceCategory(
        title="Cerrajería",
        description="Servicios de cerrajería",
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

service_1 = Service(
    user_id=2,
    service_category_id=14,  # Pedicuría/Manicuría
    approved=False,
    rejected_message="No cumple con las políticas de la plataforma",
    title="Pedicura completa con esmaltado permanente",
    description="Disfruta de pies hermosos y bien cuidados con una pedicura de alta calidad que incluye esmaltado duradero.",
    photo_url="https://cuponassets.cuponatic-latam.com/backendCl/uploads/imagenes_descuentos/122441/c54ca51efae45d8c62a7472bf0680442679feb96.XL2.jpg",
    availability_time_start="00:00",
    availability_time_end="24:00",
    availability_days="Lunes,Jueves,Sabado,Domingo"
)
service_2 = Service(
    user_id=2,
    service_category_id=15,  # Peluqueria
    approved=False,
    rejected_message="No cumple con las políticas de la plataforma",
    title="Tratamiento de keratina para cabello dañado",
    description="Restaura la salud y el brillo de tu cabello con un tratamiento de keratina profesional.",
    photo_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQP8kKT3GhVr3rd9avyBSv2exwgdYkGvVWNOy1rJT0Sdw&s",
    availability_time_start="00:00",
    availability_time_end="24:00",
    availability_days="Martes,Jueves,Viernes,Sabado,Domingo"
)
service_3 = Service(
    user_id=3,
    service_category_id=1,  # Plomeria
    approved=True,
    title="Reparación de cañerías de agua caliente",
    description="Solución rápida para problemas de fugas o averías en las tuberías de agua caliente de tu hogar.",
    photo_url="https://es.statefarm.com/content/dam/sf-library/en-us/secure/legacy/simple-insights/136-home-plumbing-checkup-wide.jpg",
    availability_time_start="00:00",
    availability_time_end="24:00",
    availability_days="Lunes,Martes,Jueves,Sabado,Domingo"
)
service_4 = Service(
    user_id=3,
    service_category_id=2,  # Pintureria
    approved=True,
    title="Pintura de interiores",
    description="Renueva tus espacios con una nueva capa de pintura para tu habitación, agregando frescura y estilo.",
    photo_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRveAictltnyrRcVuL3lf8odlAADaMV2Xr5WP0-n5Z7Bw&s",
    availability_time_start="08:00",
    availability_time_end="19:00",
    availability_days="Miercoles,Viernes"
)
service_5 = Service(
    user_id=3,
    service_category_id=3,  # Albanileria
    approved=True,
    title="Reparación de grietas en el techo",
    description="Resuelve problemas de filtraciones y deterioro con la reparación profesional de grietas en el techo.",
    photo_url="https://www.cemix.com/wp-content/uploads/2022/10/mejor-sellador-de-grietas-para-techos-.jpg",
    availability_time_start="08:00",
    availability_time_end="19:00",
    availability_days="Miercoles,Viernes"
)
service_6 = Service(
    user_id=3,
    service_category_id=4,  # Carpinteria
    approved=True,
    title="Fabricación de muebles a medida para cocina",
    description="Optimiza tu espacio y estilo con muebles personalizados para tu cocina, creados con habilidad artesanal.",
    photo_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvboifJL6e4vit3VGPR-RqK0mkLTPsIM0-0y6QLoNh2w&s",
    availability_time_start="08:00",
    availability_time_end="19:00",
    availability_days="Miercoles,Viernes"
)
service_7 = Service(
    user_id=3,
    service_category_id=5,  # Gasista
    approved=True,
    title="Instalación de cañerías de gas para cocina",
    description="Asegura una instalación segura y eficiente de cañerías de gas en tu cocina para un funcionamiento óptimo.",
    photo_url="https://www.pypesa.com/contenido/fb8a47360_blog_.jpg",
    availability_time_start="07:00",
    availability_time_end="16:00",
    availability_days="Lunes,Martes,Jueves"
)

service_8 = Service(
    user_id=3,
    service_category_id=6,  # Mecanico
    approved=True,
    title="Reparación de sistema de frenos",
    description="Garantiza tu seguridad en la carretera con una reparación completa y precisa del sistema de frenos de tu vehículo.",
    photo_url="https://blog.reparacion-vehiculos.es/hubfs/Im%C3%A1genes_Post/Enero_2016/reparacion_de_frenos.jpg",
    availability_time_start="07:00",
    availability_time_end="16:00",
    availability_days="Lunes,Martes,Jueves"
)
service_9 = Service(
    user_id=4,
    service_category_id=16,  # Abogados
    approved=True,
    title="Asesoramiento legal en casos de divorcio",
    description="Orientación experta para enfrentar los desafíos legales durante un proceso de divorcio.",
    photo_url="https://abogadoaly.com/wp-content/uploads/2020/03/Depositphotos_190058808_l-2015.jpg",
    availability_time_start="08:00",
    availability_time_end="18:00",
    availability_days="Lunes,Martes,Miercoles,Jueves,Viernes"
)
service_10 = Service(
    user_id=5,
    service_category_id=7,  # Electricista
    approved=True,
    title="Instalación de sistema de iluminación LED en hogar",
    description="Ahorra energía y moderniza tu hogar con la instalación de un sistema de iluminación LED eficiente.",
    photo_url="https://img.freepik.com/fotos-premium/sala-cine-casa-iluminacion-led-colores-hogar-inteligente_916189-435.jpg?w=360",
    availability_time_start="00:00",
    availability_time_end="18:00",
    availability_days="Lunes,Miercoles,Viernes,Domingo"
)
service_11 = Service(
    user_id=5,
    service_category_id=8,  # Cerrajeria
    approved=True,
    title="Duplicado de llaves para puerta principal",
    description="Evita contratiempos con un duplicado rápido y preciso de tus llaves principales realizado por cerrajeros expertos.",
    photo_url="https://masencarnacion.s3.us-west-2.amazonaws.com/uploads/public/638/09d/8d5/63809d8d594c3195931735.jpg",
    availability_time_start="10:00",
    availability_time_end="18:00",
    availability_days="Martes"
)
service_12 = Service(
    user_id=5,
    service_category_id=9,  # Reparacion de electrodomesticos
    approved=None,
    title="Reparación de lavadora con problemas de centrifugado",
    description="Devuelve el funcionamiento óptimo a tu lavadora con una reparación profesional de problemas de centrifugado.",
    photo_url="https://thumbs.dreamstime.com/b/servicio-de-reparacion-lavadora-joven-mujer-reparaci%C3%B3n-trabajador-218463087.jpg",
    availability_time_start="10:00",
    availability_time_end="18:00",
    availability_days="Jueves"
)
service_13 = Service(
    user_id=6,
    service_category_id=12,  # Decoracion de interiores
    approved=None,
    title="Asesoramiento en selección de colores y mobiliario para renovar tu hogar",
    description="Obtén recomendaciones profesionales sobre colores, muebles y accesorios para renovar y revitalizar tu hogar de acuerdo a tus gustos y necesidades.",
    photo_url="https://content.elmueble.com/medio/2024/04/08/salon-moderno-pequeno-con-butacas-puf-y-boveda-catalana_ff8d0a80_00573567_240408153401_600x600.jpg",
    availability_time_start="14:00",
    availability_time_end="18:00",
    availability_days="Lunes,Martes,Miercoles,Jueves,Viernes"
)
service_14 = Service(
    user_id=6,
    service_category_id=9,  # Reparacion de electrodomesticos
    approved=None,
    title="Reparación de aparatos electrónicos",
    description="Reparación de TVs, Radios, todo tipo de aparatos electrónicos",
    photo_url="https://content.elmueble.com/medio/2024/04/08/salon-moderno-pequeno-con-butacas-puf-y-boveda-catalana_ff8d0a80_00573567_240408153401_600x600.jpg",
    availability_time_start="14:00",
    availability_time_end="18:00",
    availability_days="Lunes,Martes,Miercoles,Jueves,Viernes"
)
service_15 = Service(
    user_id=6,
    service_category_id=9,  # Reparacion de electrodomesticos
    approved=None,
    title="Reparación de electrodomésticos",
    description="Reparación de TVs, Radios, todo tipo de aparatos electrónicos",
    photo_url="https://content.elmueble.com/medio/2024/04/08/salon-moderno-pequeno-con-butacas-puf-y-boveda-catalana_ff8d0a80_00573567_240408153401_600x600.jpg",
    availability_time_start="14:00",
    availability_time_end="18:00",
    availability_days="Lunes,Martes,Miercoles,Jueves,Viernes"
)

services = [
    service_1,
    service_2,
    service_3,
    service_4,
    service_5,
    service_6,
    service_7,
    service_8,
    service_9,
    service_10,
    service_11,
    service_12,
    service_13,
    service_14,
    service_15
]

rates = [
    Rate(
        user=user_1,
        service=service_1,
        rate=4,
        message="Muy buen sevicio, lo recomiendo pero la próxima espero más puntualidad.",
        approved=True,
        user_name_to_display="Julia Benavídez"
    ),
    Rate(
        user=user_2,
        service=service_2,
        rate=5,
        message="Muy bueno, recomiendo!",
        approved=True,
        user_name_to_display="Mario Delgado"
    ),
    Rate(
        user=user_2,
        service=service_3,
        rate=1,
        message="No vayan, un desastre!",
        approved=True,
        user_name_to_display="Mario Delgado"
    ),
    Rate(
        user=user_2,
        service=service_4,
        rate=1,
        message="No vayan, un desastre!!!",
        approved=True,
        user_name_to_display="Mario Delgado"
    ),
    Rate(
        user=user_3,
        service=service_5,
        rate=3,
        message="Aceptable...",
        approved=False,
        user_name_to_display="Augusto Molina"
    ),
    Rate(
        user=user_3,
        service=service_4,
        rate=4,
        message="Muy buena atención, recomiendo!",
        approved=None,
        user_name_to_display="Augusto Molina"
    ),
    Rate(
        user=user_1,
        service=service_10,
        rate=5,
        message="Excelente servicio, muy recomendable!",
        approved=True,
        user_name_to_display="Julia Benavídez"

    ),
    Rate(
        user=user_2,
        service=service_10,
        rate=3,
        message="Buen servicio, pero un poco caro",
        approved=True,
        user_name_to_display="Mario Delgado"
    ),
    Rate(
        user=user_3,
        service=service_10,
        rate=5,
        message="Excelente atencion, muy amable!",
        approved=True,
        user_name_to_display="Augusto Molina"
    ),
]

favorites = [
    Favorite(
        user=user_1,
        service=service_3,
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

        for rate in rates:
            session.add(rate)
            session.commit()

        for favorite in favorites:
            session.add(favorite)
            session.commit()
