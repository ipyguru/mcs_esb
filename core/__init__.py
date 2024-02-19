from enum import Enum


class ProductTypes(Enum):
    PRODUCT = "PRODUCT"  # товар
    SERVICE = "SERVICE"  # услуга
    OPERATION = "OPERATION"  # операция
    MATERIAL = "MATERIAL"  # материал
    EQUIPMENT = "EQUIPMENT"  # оборудование

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def get_name(cls, value):
        return cls(value).name

    @classmethod
    def get_value(cls, name):
        return cls[name].value
