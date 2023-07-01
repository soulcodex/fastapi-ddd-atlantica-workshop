from pydantic import BaseModel, Field
from typing import Text, List, Optional


class BeerVolume(BaseModel):
    value: float
    unit: Text


class Beer(BaseModel):
    id: int
    name: Text
    description: Text
    image_url: Optional[Text]
    ph: Optional[float]
    volume: BeerVolume


class BeerCollection(BaseModel):
    items: List[Beer]
    count: int
