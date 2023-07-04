from shared.domain.errors import DomainError


class InvalidShoeSize(DomainError):
    __message__ = 'Invalid shoe size specified.'

    @classmethod
    def from_shoe_size(cls, size: int) -> 'InvalidShoeSize':
        return cls(message=cls.__message__, context={'shoe_size': size})


class ShoeNotExist(DomainError):
    __message__ = 'Shoe not exist.'

    @classmethod
    def from_shoe_id(cls, shoe_id: str) -> 'ShoeNotExist':
        return ShoeNotExist(message=cls.__message__, context={'shoe_id': shoe_id})
