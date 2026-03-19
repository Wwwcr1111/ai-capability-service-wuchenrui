from abc import ABC, abstractmethod
from typing import Any


class BaseCapability(ABC):
    name: str

    @abstractmethod
    def run(self, payload: dict[str, Any]) -> Any:
        raise NotImplementedError
