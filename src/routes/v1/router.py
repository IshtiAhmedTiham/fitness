from fastapi import APIRouter
from src.controllers.v1 import user_controller

router = APIRouter()

router.include_router(user_controller.router, prefix="/user", tags=["user"])