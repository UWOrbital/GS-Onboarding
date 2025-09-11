# Data models used in the onboarding
# NOTE: This file should not be modified
from datetime import datetime
from pydantic import model_validator
from sqlmodel import Field

from backend.data.base_model import BaseSQLModel
from backend.data.enums import CommandStatus


class MainCommand(BaseSQLModel, table=True):
    """
    Main command model.
    This table represents all the possible commands that can be issued.

    List of commands: https://doc   s.google.com/spreadsheets/d/1XWXgp3--NHZ4XlxOyBYPS-M_LOU_ai-I6TcvotKhR1s/edit?gid=564815068#gid=564815068
    """

    id: int | None = Field(
        default=None, primary_key=True
    )  # NOTE: Must be None for autoincrement
    name: str
    params: str | None = None
    format: str | None = None
    data_size: int
    total_size: int

    @model_validator(mode="after")
    def validate_params_format(self):
        """
        Check that params and format are both None or that the params and format have the same number of comma seperated values.
        In either of these cases return self. Otherwise raise a ValueError.
        The format of the comma seperated values is "data1,data2" so no spaces between data and the commas.
        """
        num_values = 0
        if self.params != None:
            if self.format == None: raise ValueError
            if len(self.format.split(",")) != len(self.params.split(",")): raise ValueError
        else:
            if self.format != None: raise ValueError
        return self


class Command(BaseSQLModel, table=True):
    """
    An instance of a MainCommand.
    This table holds the data related to actual commands sent from the ground station up to the OBC.
    """
    id: int | None = Field(
        default=None, primary_key=True
    )  # NOTE: Must be None for autoincrement
    command_type: int = Field(
        foreign_key="maincommand.id"
    )  # Forign key must be a string
    status: CommandStatus = CommandStatus.PENDING
    params: str | None = None
    created_on: datetime = datetime.now()
    updated_on: datetime = datetime.now()
