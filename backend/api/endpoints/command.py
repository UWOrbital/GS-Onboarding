from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Annotated

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

    :return: Returns a list of commands
    """
    query = select(Command)
    items = db.exec(query).all()
    return {"data": items}


@command_router.post("/", response_model=CommandSingleResponse)
def create_command(payload: CommandRequest, db: Annotated[Session, Depends(get_db)]):
    """
    Creates an item with the given payload in the database and returns this payload after pulling it from the database 

    :param payload: The data used to create an item
    :return: returns a json object with field of "data" under which there is the payload now pulled from the database 
    """
    # TODO:(Member) Implement this endpoint

    item = Command(**payload.model_dump())


    db.add(item)
    db.commit()
    db.refresh(item)
    return {"data": item}

    """
    command = Command(command_type = payload.command_type, params = payload.params)
    db.add(command)
    db.commit()
    statement = select(Command).where(Command.id == command.id)
    results = db.execute(statement).scalars().first()

    return{"data": results}

    """

                      


@command_router.delete("/{id}", response_model=CommandListResponse)
def delete_command(id: int, db: Annotated[Session, Depends(get_db)]):
    """
    Deletes the item with the given id if it exists. Otherwise raises a 404 error.

    :param id: The id of the item to delete
    :return: returns the list of commands after deleting the item
    """
    # TODO:(Member) Implement this endpoint

    result = db.execute(select(Command).where(Command.id == id))
    item = result.scalars().first()
    
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found.")

    db.delete(item)
    db.commit()
    return{"data": db.execute(select(Command)).scalars().all()}