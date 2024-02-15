from pydantic import BaseModel, Field
from typing import Union


class Item(BaseModel):
    name: str
    price: int = Field(..., gt=0, description="The price must be greater than zero")
    is_offer: Union[bool, None] = None
