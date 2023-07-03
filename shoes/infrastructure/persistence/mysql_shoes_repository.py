from typing import Any, Optional, Dict, Text
from shoes.domain.value_object import ShoeId
from shoes.domain.shoe import ShoeRepository, Shoe
from shared.infrastructure.mysql.async_repository import MysqlAsyncRepository


class MysqlShoesRepository(ShoeRepository, MysqlAsyncRepository):
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

    async def find(self, shoe_id: ShoeId) -> Shoe:
        async with self._connection.reader.cursor() as cursor:
            query = f""" 
                SELECT ${",".join(self.__fields)} FROM `${self.table_name}`
                WHERE id = ${shoe_id}
            """
            await cursor.execute(query)
            item: Optional[Dict[Text, Any]] = await cursor.fetchone()

            if item is None:
                raise

            return Shoe.from_primitives(**item)
