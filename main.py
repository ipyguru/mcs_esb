from fastapi import FastAPI

from core.settings import settings

from api_v1 import router as api_v1_router


app = FastAPI(title="Шина предприятия", version="0.1.0")


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
