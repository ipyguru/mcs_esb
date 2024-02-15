from typing import Union

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductUpdatePartial(ProductBase):
    name: Union[str, None] = None
