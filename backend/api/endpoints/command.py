from fastapi import APIRouter, Depends, HTTPException
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
    Gets all the commands in the database
    """
    query = select(Command)
    items = db.exec(query).all()
    return {"data": items}


@command_router.post("/", response_model=CommandSingleResponse)
def create_command(payload: CommandRequest, db: Session = Depends(get_db)):
    """
    Creates a new command in the database and returns it
    """
    # Create a Command instance from the request payload
    cmd = Command(
        command_type=payload.command_type,
        params=payload.params
    )

    # Add and commit to the database
    db.add(cmd)
    db.commit()
    db.refresh(cmd)  # refresh to get auto-generated fields like id

    # Return the new command wrapped in the response model format
    return {"data": cmd}


@command_router.delete("/{id}", response_model=CommandListResponse)
def delete_command(id: int, db: Session = Depends(get_db)):
    """
    Deletes a command by ID and returns the remaining commands
    """
    # Fetch the command to delete
    cmd = db.get(Command, id)
    if not cmd:
        raise HTTPException(status_code=404, detail=f"Command with id={id} not found")

    # Delete it
    db.delete(cmd)
    db.commit()

    # Return remaining commands
    remaining_cmds = db.exec(select(Command)).all()
    return {"data": remaining_cmds}

