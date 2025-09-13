from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from fastapi import HTTPException

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
def create_command(payload: CommandRequest, db: Session = Depends(get_db)):
    """
    Creates an item with the given payload in the database and returns this payload after pulling it from the database 

    :param payload: The data used to create an item
    :return: returns a json object with field of "data" under which there is the payload now pulled from the database 
    """
    command = Command(command_type = payload.command_type, params = payload.params)
    db.add(command)
    db.commit()
    query = select(Command).where(Command.params == payload.params)
    command_request = db.exec(query).first()
    return {"data": command_request}

@command_router.delete("/{id}", response_model=CommandListResponse)
def delete_command(id: int, db: Session = Depends(get_db)):
    """
    Deletes the item with the given id if it exists. Otherwise raises a 404 error.

    :param id: The id of the item to delete
    :return: returns the list of commands after deleting the item
    """
    query = select(Command).where(Command.id == id)
    item_to_delete = db.exec(query).first()
    if item_to_delete == None: raise HTTPException(status_code=404, detail="Command with the following ID not found")
    else:
        db.delete(item_to_delete)
        db.commit()
    
    return get_commands(db=db)
    
    
