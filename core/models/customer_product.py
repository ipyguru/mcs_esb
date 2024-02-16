from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, ForeignKey


class CustomerProduct(Base):
    __tablename__ = "customer_products"

    name: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    def __repr__(self):
        return f"<CustomerProduct(name={self.name})>"
