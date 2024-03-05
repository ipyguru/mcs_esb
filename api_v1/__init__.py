from fastapi import APIRouter

from .esb.views import router as esb_router

router = APIRouter()
router.include_router(router=esb_router)
