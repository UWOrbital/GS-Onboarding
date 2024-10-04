from _pytest import scope
from sqlmodel import SQLModel, Session, create_engine
import pytest
from datetime import datetime

from backend.data.data_models import MainCommand, Command


@pytest.fixture
def db_engine():
    sqlite_file_name = "sqlite://"  # In memory db for testing
    engine = create_engine(sqlite_file_name)
    return engine


@pytest.fixture
def unix_time():
    default_datetime = datetime.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    return int(default_datetime.timestamp())


@pytest.fixture
def main_commands():
    return [
        MainCommand(
            id=1,
            name="RTC Sync",
            params="time",
            format="int 7 bytes",
            data_size=7,
            total_size=8,
        ),
        MainCommand(
            id=2,
            name="Manually activate an emergency mode for a specified amount of time",
            params="mode_state_number,time",
            format="int 1 byte, int 7 bytes",
            data_size=8,
            total_size=9,
        ),
    ]


@pytest.fixture
def commands(unix_time):
    return [
        Command(id=1, command_type=1, params=f"{unix_time}"),  # RTC Sync for 2021-01-01
        Command(
            id=2, command_type=2, params=f"1,{unix_time}"
        ),  # Emergency mode for 2021-01-01
    ]


@pytest.fixture(scope="function", autouse=True)
def setup_db(db_engine, main_commands, commands):
    SQLModel.metadata.create_all(db_engine)
    with Session(db_engine) as session:
        session.add_all(main_commands)
        session.commit()
        session.add_all(commands)
        session.commit()
