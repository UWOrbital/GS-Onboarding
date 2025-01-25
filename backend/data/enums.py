# Enums used in the onboarding challenge
from enum import Enum, auto


class CommandStatus(Enum):
    """
    Enum representing the command status.

    @warning This enum shouldn't be modified
    """

    PENDING = auto()
    SCHEDULED = auto()
    ONGOING = auto()
    CANCELLED = auto()
    FAILED = auto()
    COMPLETED = auto()
