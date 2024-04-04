from datetime import datetime

from sqlmodel import SQLModel, create_engine, Session

from .auth import auth_handler
from .models.users import User

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)


def seed_db():
    users = [
        User(
            username="john_doe",
            password=auth_handler.get_password_hash("password"),
            email="john_doe@example.com",
            created_at=datetime.now(),
            course_rates=[],
            course_favorites=[],
            course_subscriptions=[]
        )
    ]

    with Session(engine) as session:
        for user in users:
            session.add(user)
        session.commit()
