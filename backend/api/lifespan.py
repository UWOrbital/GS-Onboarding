from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
import backend.data.data_models
from backend.data.engine import get_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    print("Starting the app")
    SQLModel.metadata.create_all(get_db().connection())
    yield
    print("Stopping the app")
