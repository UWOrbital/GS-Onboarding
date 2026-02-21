from typing import Final
from sqlmodel import Session, create_engine

SQL_PATH: Final[str] = "sqlite:///sqlite.db"


def get_db() -> Session:
    engine = create_engine(SQL_PATH)
    with Session(engine) as session:
        return session
