from contextlib import asynccontextmanager
from datetime import datetime
from typing import Final
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, delete
import pytest
from backend.api.lifespan import create_startup
from backend.api.setup import setup_middlewares, setup_routes
from backend.data.data_models import Command, MainCommand
from backend.data.engine import get_db
from backend.data.mock_data import commands, main_commands
from backend.utils.time import to_unix_time
from json import loads
from sqlmodel.pool import StaticPool

TESTING_SQL_PATH: Final[str] = "sqlite:///testing.db" 

def get_mock_db() -> Session:
    engine = create_engine(TESTING_SQL_PATH, connect_args={"check_same_thread": False}, poolclass=StaticPool)
    with Session(engine) as session:
        return session

@pytest.fixture
def mock_db() -> Session:
    return get_mock_db()


@pytest.fixture
def default_datetime():
    default_time = "2024-01-01T00:00:00"
    return datetime.strptime(default_time, "%Y-%m-%dT%H:%M:%S")


@asynccontextmanager
async def lifespan(_: FastAPI):
    db = get_mock_db()
    create_startup(db)
    yield
    del_main_command = delete(MainCommand)
    db.exec(del_main_command)
    db.commit()
    del_command = delete(Command)
    db.exec(del_command)
    db.commit()


@pytest.fixture
def fastapi_app():
    app = FastAPI(lifespan=lifespan)
    app.dependency_overrides[get_db] = get_mock_db 
    setup_routes(app)
    setup_middlewares(app)
    return app

@pytest.fixture
def fastapi_test_client(fastapi_app):
    return TestClient(fastapi_app)

@pytest.fixture
def commands_json(default_datetime):
    commands_with_id = []
    for i, val in enumerate(commands(to_unix_time(default_datetime)), start=1):
        val.id = i
        serialize_command = val.model_dump_json()
        command = loads(serialize_command)
        commands_with_id.append(command)
    return commands_with_id


@pytest.fixture(scope="function", autouse=True)
def setup_db(mock_db: Session, default_datetime):
    SQLModel.metadata.create_all(mock_db.connection())
    with mock_db as session:
        session.add_all(main_commands())
        session.commit()
        session.add_all(commands(to_unix_time(default_datetime)))
        session.commit()
        yield
        del_main_command = delete(MainCommand)
        session.exec(del_main_command)
        session.commit()
        del_command = delete(Command)
        session.exec(del_command)
        session.commit()

    
