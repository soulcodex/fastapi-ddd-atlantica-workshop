from unittest.mock import patch, AsyncMock
from unittest import IsolatedAsyncioTestCase
from shoes.infrastructure.pytest.factory import ShoeObjectMother

from shoes.domain.errors import ShoeNotExist
from shoes.domain.shoe import ShoesRepository
from shoes.application.shoe_response import ShoeResponse
from shoes.application.find_shoe_by_id import FindShoeByIdQuery, FindShoeByIdQueryHandler


class TestFindShoeByIdQueryHandler(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.shoe_factory = ShoeObjectMother()

    @patch(f'{ShoesRepository.__module__}.{ShoesRepository.__name__}.find')
    async def test_fetch_one_shoe_by_id_successfully(self, repository: AsyncMock) -> None:
        # Given
        shoe = self.shoe_factory.random_shoe()
        repository.find.return_value = shoe

        # When
        query = FindShoeByIdQuery(shoe_id=shoe.id.value)
        handler = FindShoeByIdQueryHandler(repository=repository)
        handled = await handler.handle(query)

        # Then
        repository.find.assert_awaited_with(shoe_id=shoe.id)
        self.assertIsInstance(handled, ShoeResponse)

    @patch(f'{ShoesRepository.__module__}.{ShoesRepository.__name__}.find')
    async def test_fetch_one_shoe_by_id_fails_due_to_not_exists(self, repository: AsyncMock) -> None:
        with self.assertRaises(ShoeNotExist) as _:
            # Given
            shoe = self.shoe_factory.random_shoe()
            repository.find.side_effect = ShoeNotExist.from_shoe_id(shoe.id.value)

            # When
            query = FindShoeByIdQuery(shoe_id=shoe.id.value)
            handler = FindShoeByIdQueryHandler(repository=repository)
            await handler.handle(query)

            # Then
            repository.find.assert_awaited_with(shoe_id=shoe.id)
