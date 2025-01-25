from pydantic import BaseModel


class CommandRequest(BaseModel):
    """
    Model representing the command to be created
    """

    command_type: int
    params: str | None = None
