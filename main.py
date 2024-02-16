from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

from core import admin as admin_views
from core.models import helper
from core.settings import settings

from api_v1 import router as api_v1_router


"""
Создание и инициализация базы данных:
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Мы используем alembic для миграции базы данных."""
    # async with helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

"""
Подключение админки:
"""
admin = Admin(app, helper.engine, title="Администрирование")
admin.add_view(admin_views.ProductAdmin)
admin.add_view(admin_views.CustomerAdmin)
admin.add_view(admin_views.CustomerProductAdmin)

"""
Подключение роутов:
"""
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)


"""
Запуск сервера:
"""
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
