from pydantic import BaseModel

from backend.data.data_models import Command, MainCommand


class CommandListResponse(BaseModel):
    """
    List of all commands
    """

    data: list[Command]


class MainCommandListResponse(BaseModel):
    """
    List of main commands
    """

    data: list[MainCommand]


class CommandSingleResponse(BaseModel):
    """
    Single command 
    """
    data: Command
