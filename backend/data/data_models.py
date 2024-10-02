# Data models used in the onboarding
# NOTE: This file should not be modified
from datetime import datetime
from sqlmodel import Field, SQLModel

from backend.data.enums import CommandStatus


class MainCommand(SQLModel, table=True):
    """
    Main command model.
    This table represents all the possible commands that can be issued.

    List of commands: https://docs.google.com/spreadsheets/d/1XWXgp3--NHZ4XlxOyBYPS-M_LOU_ai-I6TcvotKhR1s/edit?gid=564815068#gid=564815068
    """

    id: int | None = Field(default=None, primary_key=True)
    name: str
    params: str | None = None
    format: str | None = None
    data_size: int
    total_size: int


class Command(SQLModel, table=True):
    """
    An instance of a MainCommand.
    This table holds the data related to actual commands sent from the ground station up to the OBC.
    """

    id: int | None = Field(primary_key=True)
    command_type: int = Field(foreign_key=MainCommand.id)
    status: CommandStatus = CommandStatus.PENDING
    params: str | None = None
    created_on: datetime = datetime.now()
    updated_on: datetime = datetime.now()
