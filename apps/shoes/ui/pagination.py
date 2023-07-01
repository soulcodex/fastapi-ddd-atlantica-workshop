from pydantic import BaseModel, Field


class Pagination(BaseModel):
    page: int = Field(default=1, description='Page number')
    per_page: int = Field(default=10, description='Items per page')
