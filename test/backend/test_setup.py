# Test to make sure the conftest.py setup is correct
import pytest
from sqlmodel import Session, select
from backend.data.data_models import MainCommand, Command

from backend.utils.time import to_unix_time


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
    mock_db: Session, command_id, name, params, format, data_size, total_size
):
    main_command = mock_db.get(MainCommand, command_id)
    assert main_command
    assert main_command.name == name
    assert main_command.params == params
    assert main_command.format == format
    assert main_command.data_size == data_size
    assert main_command.total_size == total_size
    query = select(MainCommand)
    all_main_commands = mock_db.exec(query).all()
    assert len(all_main_commands) == 2


@pytest.mark.parametrize(
    "id, command_type, params", [(1, 1, "{unix_time}"), [2, 2, "1,{unix_time}"]]
)
def test_command_setup(mock_db, id, command_type, params, default_datetime):
    command = mock_db.get(Command, id)
    assert command
    assert command.command_type == command_type
    assert command.params == params.format(unix_time=to_unix_time(default_datetime))


