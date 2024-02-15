from pydantic import BaseModel, Field, ConfigDict
from typing import Union


class ProductBase(BaseModel):
    name: str


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductCreate(ProductBase):
    pass
