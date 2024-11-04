from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from backend.api.models.response_model import MainCommandListResponse
from backend.data.data_models import MainCommand
from backend.data.engine import get_db

main_command_router = APIRouter(tags=["Main Commands"])


@main_command_router.get("/", response_model=MainCommandListResponse)
def get_main_commands(db: Session = Depends(get_db)):
    """
    Gets all the main commands that can be created.

    @return Returns a list of main commands
    """
    query = select(MainCommand)
    items = db.exec(query).all()
    return {"data": items}
