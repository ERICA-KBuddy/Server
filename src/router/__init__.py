# --------------------------------------------------------------------------
# Backend Application과 router을 연결하는 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from fastapi import APIRouter

from .user import user_router
from .area import area_router
from .review import review_router
from .order import order_router
from .point import point_router
from .itinerary import itinerary_router

router = APIRouter(prefix="/kbuddy/api/v1")

router.include_router(user_router, tags=["user"])
router.include_router(area_router, tags=["area"])
router.include_router(review_router, tags=["review"])
router.include_router(order_router, tags=["order"])
router.include_router(point_router, tags=["point"])
router.include_router(itinerary_router, tags=["itinerary"])


@router.get(
    "/ping",
    summary="Server health check",
    description="FastAPI 서버가 정상적으로 동작하는지 확인합니다.",
    response_model=dict,
    responses={
        200: {
            "description": "Ping Success",
            "content": {"application/json": {"example": {"ping": "pong"}}},
        },
    },
)
async def ping():
    return {"ping": "pong"}
