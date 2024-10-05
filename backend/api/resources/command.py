from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from backend.api.models.request_model import CommandRequest
from backend.api.models.response_model import CommandListResponse
from backend.data.data_models import Command
from backend.data.engine import get_db

command_router = APIRouter(tags=["Commands"])


@command_router.get("/", response_model=CommandListResponse)
async def get_items(db: Session = Depends(get_db)):
    """
    Gets all the items

    @return Returns a list of commands
    """
    query = select(Command)
    items = db.exec(query).all()
    print(f"Items: {items}")
    return {"data": items}


@command_router.post("/", response_model=Command)
async def create_item(payload: CommandRequest):
    """
    Creates an item with the given payload and returns the payload with some other information

    @param payload: The data used to create an item
    @return returns the data with some other information
    """
    # TODO: Implement this endpoint


@command_router.delete("/{id}")
async def delete_item(id: int):
    """
    Deletes the item with the given id if it exists. Otherwise raises a 404 error.

    @param id: The id of the item to delete
    """
    # TODO: Implement this endpoint
