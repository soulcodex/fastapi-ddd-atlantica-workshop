import aiomysql
from pypika import MySQLQuery, Table
from databases.interfaces import Record
from typing import Any, Optional, Dict, Text, List, Mapping

from shoes.domain.value_object import ShoeId
from shoes.domain.errors import ShoeNotExist
from shoes.domain.shoe import ShoesRepository, Shoe
from shared.infrastructure.mysql.async_repository import MysqlAsyncRepository


# noinspection PyProtectedMember
class MysqlShoesRepository(ShoesRepository, MysqlAsyncRepository):
    __fields = [
        "id",
        "name",
        "color",
        "size",
        "price",
        "available",
        "created_at",
        "updated_at"
    ]

    async def fields_list(self, shoe: Shoe) -> List[Any]:
        return [
            shoe.id.value,
            shoe.name.value,
            shoe.color.value,
            shoe.size.value,
            shoe.price.raw_value,
            shoe.available.value,
            shoe.created_at.value,
            shoe.updated_at.value
        ]

    async def find(self, shoe_id: ShoeId) -> Shoe:
        async with self._pool.connection() as connection:
            builder = await self.query_builder()
            query = builder \
                .select(*self.__fields) \
                .where(builder.id == shoe_id.value) \
                .get_sql()

            row: Optional[Record] = await connection.fetch_one(query=query)

            print(row)
            if row is None:
                raise ShoeNotExist.from_shoe_id(shoe_id=shoe_id.value)

            # noinspection PyProtectedMember
            item: Mapping = row._mapping
            return Shoe.from_primitives(**{**item, 'size': int(item.get('size'))})

    async def save(self, shoe: 'Shoe') -> None:
        async with self._pool.connection() as connection:
            builder = await self.query_builder()
            fields = await self.fields_list(shoe)
            query = builder.insert(*fields).get_sql()

            async def tx() -> None:
                await connection.execute(query)

            try:
                await self._transaction(tx)
            except aiomysql.Error:
                pass  # raise domain exception
