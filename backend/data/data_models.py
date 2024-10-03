# Data models used in the onboarding
# NOTE: This file should not be modified
from datetime import datetime
from typing import Self
from pydantic import model_validator
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

    @model_validator(mode="after")
    def validate_params_format(self) -> Self:
        """Check that params and format are both None or that the params and format have the same number of comma seperated values"""
        if self.params is None and self.format is None:
            return self
        assert self.params is not None
        assert self.format is not None
        assert len(self.params.split(",")) == len(self.format.split(","))
        return self


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
