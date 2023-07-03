from enum import Enum
from typing import Text, Dict, Any


class ErrorSeverity(Enum):
    CRITICAL = 'critical'
    WARNING = 'warning'


class BaseError(Exception):

    def __init__(self, message: Text, context: Dict[Text, Any]):
        self.message = message
        self.context = context
        super(BaseError).__init__(message, context)

    @classmethod
    def severity(cls) -> ErrorSeverity:
        return ErrorSeverity.CRITICAL


class DomainError(BaseError):

    @classmethod
    def severity(cls) -> ErrorSeverity:
        return ErrorSeverity.WARNING


class CriticalError(BaseError):
    pass
