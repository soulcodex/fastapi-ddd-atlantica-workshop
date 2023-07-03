from shared.domain.errors import DomainError


class InvalidShoeSize(DomainError):
    __message__ = 'Invalid shoe size specified.'

    @classmethod
    def from_shoe_size(cls, size: int) -> 'InvalidShoeSize':
        return InvalidShoeSize(message=cls.__message__, context={'shoe_size': size})
