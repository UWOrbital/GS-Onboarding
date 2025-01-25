from datetime import datetime


def to_unix_time(time: datetime) -> int:
    return int(time.timestamp())
