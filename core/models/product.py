from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(150))

    def __repr__(self):
        return f"<Product(name={self.name})>"
