from datetime import datetime
from abc import ABC, abstractmethod


class TimeProvider(ABC):

    @abstractmethod
    def now(self) -> datetime:
        pass
