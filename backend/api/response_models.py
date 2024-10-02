from pydantic import BaseModel

from backend.data.data_models import Command


class CommandListResponse(BaseModel):
    """
    List of all commands
    """

    data: list[Command]
