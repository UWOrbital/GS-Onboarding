from backend.data.data_models import Command, MainCommand


def commands(unix_time: int) -> list[Command]:
    return [
        Command(command_type=1, params=f"{unix_time}"),  # id=1, RTC Sync for 2021-01-01
        Command(
            command_type=2, params=f"1,{unix_time}"
        ),  # id=2, Emergency mode for 2021-01-01
    ]


def main_commands() -> list[MainCommand]:
    return [
        MainCommand(
            name="RTC Sync",
            params="time",
            format="int 7 bytes",
            data_size=7,
            total_size=8,
        ),  # Will have id of 1
        MainCommand(
            name="Manually activate an emergency mode for a specified amount of time",
            params="mode_state_number,time",
            format="int 1 byte, int 7 bytes",
            data_size=8,
            total_size=9,
        ),  # Will have id of 2
    ]
