from sqladmin import ModelView

from core.models import Product, Customer, CustomerProduct


class ProductAdmin(ModelView, model=Product):
    name = "Товар"
    name_plural = "Товары"

    column_list = ["id", "name", "type", "guid_bp"]
    column_searchable_list = [
        "name",
        "type",
    ]

    column_sortable_list = ["id", "name"]
    column_default_sort = ("id", True)

    column_details_list = [
        "type",
        "id",
        "name",
        "guid_bp",
        "guid_pr",
        "customer_products",
    ]


class CustomerAdmin(ModelView, model=Customer):
    name = "Клиент"
    name_plural = "Клиенты"

    column_list = ["id", "name", "inn"]
    column_searchable_list = ["name", "inn"]
    column_sortable_list = ["id", "name"]
    column_default_sort = ("id", True)


class CustomerProductAdmin(ModelView, model=CustomerProduct):
    name = "Товар клиента"
    name_plural = "Товары клиентов"

    column_list = ["id", "name", "customer", "product"]
    column_searchable_list = ["customer", "product"]
    column_filters = ["customer", "product"]
    column_sortable_list = ["id", "customer", "product"]
    column_default_sort = ("id", True)
