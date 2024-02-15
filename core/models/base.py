from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    """
    Это базовый класс для всех моделей.
    """

    """ Он не должен создаваться в базе данных. """
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(self) -> Mapped[str]:
        """
        Имя таблицы должно быть таким же, как имя класса.
        Только с префиксом esb_.
        """
        return f"esb_{self.__name__.lower()}"

    """ Все модели должны иметь первичный ключ. """
    id: Mapped[int] = mapped_column(primary_key=True)
