from enum import Enum
from typing import Text, Dict, Any


class ErrorSeverity(Enum):
    CRITICAL = 'critical'
    WARNING = 'warning'


class BaseError(BaseException):

    def __init__(self, message: Text, context: Dict[Text, Any]):
        self.message = message
        self.context = context

    @classmethod
    def severity(cls) -> ErrorSeverity:
        return ErrorSeverity.CRITICAL


class DomainError(BaseError):

    @classmethod
    def severity(cls) -> ErrorSeverity:
        return ErrorSeverity.WARNING


class CriticalError(BaseError):
    pass
