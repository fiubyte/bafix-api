import os

from sqlmodel import SQLModel, create_engine, Session

from .auth import auth_handler
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
        email="admin@example.com",
        password=auth_handler.get_password_hash("admin"),
        roles="ADMIN"
    )
]


def seed_db():
    with Session(engine) as session:
        for user in users:
            session.add(user)
        session.commit()
