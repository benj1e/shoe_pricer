"""Sets up database connection"""

import decouple
from sqlmodel import create_engine, Session, SQLModel
from typing import Annotated
from fastapi import Depends

DATABASE_NAME = decouple.config("DATABASE_NAME")


sqlite_file_name = f"{DATABASE_NAME}"
sqlite_file_path = f"sqlite:///test/{sqlite_file_name}"


connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_file_path, connect_args=connect_args)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
