from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from backend.api.models.request_model import CommandRequest
from backend.api.models.response_model import CommandListResponse, CommandSingleResponse
from backend.data.data_models import Command
from backend.data.engine import get_db

# Prefix: "/commands"
command_router = APIRouter(tags=["Commands"])


@command_router.get("/", response_model=CommandListResponse)
def get_commands(db: Session = Depends(get_db)):
    """
    Gets all the items

    @return Returns a list of commands
    """
    query = select(Command)
    items = db.exec(query).all()
    return {"data": items}


@command_router.post("/", response_model=CommandSingleResponse)
def create_command(payload: CommandRequest):
    """
    Creates an item with the given payload and returns the payload with some other information

    @param payload: The data used to create an item
    @return returns a json object with field of "data" under which there is the payload with some other information
    """
    # TODO:(Member) Implement this endpoint
                      


@command_router.delete("/{id}", response_model=CommandListResponse)
def delete_command(id: int):
    """
    Deletes the item with the given id if it exists. Otherwise raises a 404 error.

    @param id: The id of the item to delete
    @return returns the list of commands after deleting the item
    """
    # TODO:(Member) Implement this endpoint
