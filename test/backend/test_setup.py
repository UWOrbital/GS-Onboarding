# Test to make sure the conftest.py setup is correct
import pytest
from backend.data.data_models import MainCommand, Command
from sqlmodel import Session


@pytest.mark.parametrize(
    "command_id, name, params, format, data_size, total_size",
    [
        (1, "RTC Sync", "time", "int 7 bytes", 7, 8),
        (
            2,
            "Manually activate an emergency mode for a specified amount of time",
            "mode_state_number,time",
            "int 1 byte, int 7 bytes",
            8,
            9,
        ),
    ],
)
def test_main_command_setup(
    db_engine, command_id, name, params, format, data_size, total_size
):
    with Session(db_engine) as session:
        main_command = session.get(MainCommand, command_id)
        assert main_command
        assert main_command.name == name
        assert main_command.params == params
        assert main_command.format == format
        assert main_command.data_size == data_size
        assert main_command.total_size == total_size


@pytest.mark.parametrize(
    "id, command_type, params", [(1, 1, "{unix_time}"), [2, 2, "1,{unix_time}"]]
)
def test_command_setup(db_engine, id, command_type, params, unix_time):
    with Session(db_engine) as session:
        command = session.get(Command, id)
        assert command
        assert command.command_type == command_type
        assert command.params == params.format(unix_time=unix_time)
