from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.models import Base, helper
from core.settings import settings

from api_v1 import router as api_v1_router


"""
Создание и инициализация базы данных:
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

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
