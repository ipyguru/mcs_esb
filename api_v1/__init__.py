from fastapi import APIRouter

from .producer.views import router as producer_router

router = APIRouter()
router.include_router(router=producer_router, prefix="/producer")
