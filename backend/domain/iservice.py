from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class IService(ABC, Generic[T]):
    @abstractmethod
    def get(self, id: int) -> T: ...
