from datetime import datetime
from pydantic import model_validator
from sqlmodel import Field

from backend.data.base_model import BaseSQLModel
from backend.data.enums import CommandStatus


class MainCommand(BaseSQLModel, table=True):
    """
    Main command model.
    This table represents all the possible commands that can be issued.
    """

    id: int | None = Field(default=None, primary_key=True)
    name: str
    params: str | None = None
    format: str | None = None
    data_size: int
    total_size: int

    @model_validator(mode="after")
    def validate_params_format(self):
        """
        Check that params and format are both None or that the params and format have the same number of comma-separated values.
        In either of these cases return self. Otherwise raise a ValueError.
        """
        # Both None is fine
        if self.params is None and self.format is None:
            return self

        # One is None, error
        if (self.params is None) != (self.format is None):
            raise ValueError(
                f"params and format must both be None or both defined. Got params={self.params}, format={self.format}"
            )

        # Split and compare
        params_list = self.params.split(",")
        format_list = self.format.split(",")

        if len(params_list) != len(format_list):
            raise ValueError(
                f"Number of params ({len(params_list)}) does not match number of format fields ({len(format_list)})."
            )

        return self


class Command(BaseSQLModel, table=True):
    """
    An instance of a MainCommand.
    This table holds the data related to actual commands sent from the ground station up to the OBC.
    """

    id: int | None = Field(default=None, primary_key=True)
    command_type: int = Field(foreign_key="maincommand.id")
    status: CommandStatus = CommandStatus.PENDING
    params: str | None = None
    created_on: datetime = datetime.now()
    updated_on: datetime = datetime.now()


