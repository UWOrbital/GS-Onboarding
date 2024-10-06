from datetime import datetime
from sqlmodel import SQLModel, Session, create_engine
import pytest
from backend.data.mock_data import commands, main_commands
from backend.utils.time import to_unix_time


@pytest.fixture
def db_engine():
    sqlite_file_name = "sqlite://"  # In memory db for testing
    engine = create_engine(sqlite_file_name)
    return engine


@pytest.fixture
def default_datetime():
    default_time = "2024-01-01T00:00:00"
    return datetime.strptime(default_time, "%Y-%m-%dT%H:%M:%S")


@pytest.fixture(scope="function", autouse=True)
def setup_db(db_engine, default_datetime):
    SQLModel.metadata.create_all(db_engine)
    with Session(db_engine) as session:
        session.add_all(main_commands())
        session.commit()
        session.add_all(commands(to_unix_time(default_datetime)))
        session.commit()
