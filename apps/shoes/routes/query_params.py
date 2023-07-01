from fastapi import Query
from apps.shoes.ui.pagination import Pagination


async def pagination(page: int = Query(default=1), per_page: int = Query(default=10)) -> Pagination:
    return Pagination(**{"page": page, "per_page": per_page})
