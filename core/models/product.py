from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, Column

from .base import Base
from core import ProductTypes

if TYPE_CHECKING:
    from .customer_product import CustomerProduct  # noqa: F401


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(150), doc="Наименование")

    guid_pr: Mapped[str] = mapped_column(
        String(36), doc="UUID производства", nullable=False, unique=True
    )

    # BP Guid -Can empty
    guid_bp: Mapped[str] = mapped_column(
        String(36),
        doc="UUID бухгалтерии",
        default="",
        server_default="",
    )

    type: Mapped[ProductTypes] = mapped_column(
        Enum(ProductTypes), doc="Тип продукции", nullable=False
    )

    customer_products: Mapped[list["CustomerProduct"]] = relationship(
        back_populates="product"
    )

    def __repr__(self):
        return f"<Product(name={self.name})>"
