from inspect import formatannotation
from sqlmodel import SQLModel, Session, create_engine
import pytest

from backend.data.data_models import MainCommand, Command


@pytest.fixture
def db_engine():
    sqlite_file_name = "sqlite://"  # In memory db for testing
    engine = create_engine(sqlite_file_name)
    return engine


@pytest.fixture(scope="session", autouse=True)
def setup_db(db_engine):
    SQLModel.metadata.create_all(db_engine)
    with Session(db_engine) as session:
        session.add(
            MainCommand(
                id=1,
                name="RTC Sync",
                params="time",
                format="int 7 bytes",
                data_size=7,
                total_size=8,
            )
        )
        session.add(
            MainCommand(
                id=2,
                name="Manually activate an emergency mode for a specified amount of time",
                params="mode_state_number,time",
                format="int 1 byte, int 7 bytes",
                data_size=8,
                total_size=9,
            )
        )
        session.commit()
