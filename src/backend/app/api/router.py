from fastapi import APIRouter

from app.api.days import router as days_router
from app.api.meals import router as meals_router
from app.api.targets import router as targets_router


router = APIRouter(prefix="/api")
router.include_router(days_router)
router.include_router(meals_router)
router.include_router(targets_router)