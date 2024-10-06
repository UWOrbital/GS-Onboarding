import pytest
from sqlmodel import Session
from backend.data.data_models import MainCommand


def test_main_command():
    main_command = MainCommand(
        name="Test",
        params="param1,param2",
        format="int,int",
        data_size=2,
        total_size=2,
    )
    assert main_command.name == "Test"
    assert main_command.params == "param1,param2"
    assert main_command.format == "int,int"
    assert main_command.data_size == 2
    assert main_command.total_size == 2


def test_main_command_no_params_and_no_format():
    main_command = MainCommand(
        name="Test",
        data_size=2,
        total_size=2,
    )
    assert main_command.name == "Test"
    assert main_command.params is None
    assert main_command.format is None
    assert main_command.data_size == 2
    assert main_command.total_size == 2


def test_main_command_no_format(db_engine):
    with pytest.raises(ValueError), Session(db_engine) as session:
        session.add(
            MainCommand(
                name="Test",
                params="param1,param2",
                data_size=2,
                total_size=2,
            )
        )
        session.commit()


def test_main_command_no_params(db_engine):
    with pytest.raises(ValueError), Session(db_engine) as session:
        session.add(
            MainCommand(
                name="Test",
                format="int,int",
                data_size=2,
                total_size=2,
            )
        )
        session.commit()
