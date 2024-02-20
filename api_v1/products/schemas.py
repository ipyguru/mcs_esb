from typing import Annotated

from pydantic import BaseModel, ConfigDict

from core import ProductTypes


"""
Product schema
"""


class ProductBase(BaseModel):
    name: str
    type: ProductTypes


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    guid_pr: str
    guid_bp: Annotated[str, None]


class ProductPublic(Product):
    pass
    # class Config:
    #     from_attributes = True


class ProductCreate(ProductBase):
    guid_pr: str
    type: str


class ProductUpdate(ProductBase):
    pass


class ProductUpdatePartial(ProductBase):
    name: Annotated[str, None] = None
