import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration

from fastapi import FastAPI

from core.settings import settings

from api_v1 import router as api_v1_router

sentry_sdk.init(
    dsn=settings.sentry_sdk_dsn,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    integrations=[
        StarletteIntegration(transaction_style="endpoint"),
        FastApiIntegration(transaction_style="endpoint"),
    ],
)


app = FastAPI(title="Шина предприятия", version="1.0.0")


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
