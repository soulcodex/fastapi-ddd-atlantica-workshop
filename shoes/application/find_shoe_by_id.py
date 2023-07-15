from dataclasses import dataclass
from shared.domain.bus.dto import Dto
from shoes.domain.value_object import ShoeId
from shoes.domain.shoe import ShoesRepository
from shared.domain.bus.query_bus import QueryHandler
from shoes.application.shoe_response import ShoeResponse


@dataclass
class FindShoeByIdQuery(Dto):
    shoe_id: str

    @staticmethod
    def id() -> str:
        return "find_shoe_by_id_query"


class FindShoeByIdQueryHandler(QueryHandler):

    def __init__(self, repository: ShoesRepository):
        self.repository = repository

    async def handle(self, query: FindShoeByIdQuery) -> ShoeResponse:
        shoe_id = ShoeId(query.shoe_id)
        shoe = await self.repository.find(shoe_id=shoe_id)
        return ShoeResponse.from_shoe(shoe)
