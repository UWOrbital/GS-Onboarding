from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from sqlmodel import SQLModel, select
from backend.data.data_models import MainCommand
from backend.data.engine import get_db
from backend.data.mock_data import commands, main_commands
from backend.utils.time import to_unix_time


@asynccontextmanager
async def lifespan(_: FastAPI):
    print("Starting application")
    SQLModel.metadata.create_all(get_db().connection())
    default_time = "2024-01-01T00:00:00"
    default_datetime = datetime.strptime(default_time, "%Y-%m-%dT%H:%M:%S")
    unix_time = to_unix_time(default_datetime)
    # Setup the db with mock data
    with get_db() as session:
        query = select(MainCommand).limit(1)  # Check if the db is empty
        result = session.exec(query).first()
        print(result)
        if result is None:
            session.add_all(main_commands())
            session.commit()
            session.add_all(commands(unix_time))
            session.commit()
    yield
