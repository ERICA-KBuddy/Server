# --------------------------------------------------------------------------
# Point model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import point as crud
from src.crud import user as user_crud
from src.db import database
from src.router._check import check_user, auth
from src.schemas.requests import (
    PointEventCreate,
    PointEventUpdate,
    PointDetailCreate,
    PointDetailUpdate,
)
from src.schemas.responses import PointDetailSchema, PointEventSchema
from src.helper.exceptions import InternalException, ErrorCode


log = getLogger(__name__)
point_router = APIRouter(prefix="/point")


@point_router.get(
    "/events",
    response_model=List[PointEventSchema],
    summary="포인트 이벤트 전체를 불러오기",
    description="본인에게 발급된 모든 포인트 이벤트를 조회합니다.",
    dependencies=[Depends(auth)],
)
async def get_all_point_events(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(database.get_db),
):
    current_user = await check_user(request=request)
    current_user_data = await user_crud.get_user_by_email(
        db=db, user_email=current_user
    )
    result_data = await crud.get_all_point_events(
        db, str(current_user_data.id), skip=skip, limit=limit
    )
    log.info(f"Reading point events with skip: {skip} and limit: {limit}")
    return result_data


@point_router.get(
    "/events/{event_id}",
    response_model=PointEventSchema,
    summary="단일 포인트 이벤트 조회",
    description="본인에게 발급된 단일 포인트 이벤트를 조회합니다.",
    dependencies=[Depends(auth)],
)
async def read_point_event(
    request: Request, event_id: int, db: AsyncSession = Depends(database.get_db)
):
    current_user = await check_user(request=request)
    current_user_data = await user_crud.get_user_by_email(
        db=db, user_email=current_user
    )
    db_event = await crud.get_point_event(db, event_id)
    if db_event is None:
        raise InternalException(
            "해당 포인트 이벤트를 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    if db_event.user_id != current_user_data.id:
        raise InternalException(
            "본인의 포인트 이벤트만 조회 가능합니다.", error_code=ErrorCode.FORBIDDEN
        )
    return db_event


@point_router.post(
    "/events",
    response_model=PointEventSchema,
    summary="포인트 이벤트 추가",
    description="새로운 포인트 이벤트를 추가합니다.",
)
async def create_point_event(
    event: PointEventCreate, db: AsyncSession = Depends(database.get_db)
):
    return await crud.create_point_event(db, event)


@point_router.put(
    "/events/{event_id}",
    response_model=PointEventSchema,
    summary="포인트 이벤트 수정",
    description="포인트 이벤트 정보를 수정합니다.",
)
async def update_point_event(
    event_id: int,
    event: PointEventUpdate,
    db: AsyncSession = Depends(database.get_db),
):
    db_event = await crud.get_point_event(db, event_id)
    if db_event is None:
        raise InternalException(
            "해당 포인트 이벤트를 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return await crud.update_point_event(db, event_id, event)


@point_router.delete(
    "/events/{event_id}",
    status_code=204,
    summary="포인트 이벤트 삭제",
    description="포인트 이벤트를 삭제합니다.",
)
async def delete_point_event(
    event_id: int,
    db: AsyncSession = Depends(database.get_db),
):
    db_event = await crud.get_point_event(db, event_id)
    if db_event is None:
        raise InternalException(
            "해당 포인트 이벤트를 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    await crud.delete_point_event(db, event_id)
    return {"detail": "포인트 이벤트가 성공적으로 삭제되었습니다."}


@point_router.get(
    "/details",
    response_model=List[PointDetailSchema],
    summary="포인트 상세 내역 전체를 불러오기",
    description="모든 포인트 상세 내역을 조회합니다.",
)
async def get_all_point_details(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)
):
    log.info(f"Reading point details with skip: {skip} and limit: {limit}")
    return await crud.get_all_point_details(db, skip=skip, limit=limit)


@point_router.get(
    "/details/{detail_id}",
    response_model=PointDetailSchema,
    summary="단일 포인트 상세 내역 조회",
    description="단일 포인트 상세 내역을 조회합니다.",
)
async def read_point_detail(
    detail_id: int, db: AsyncSession = Depends(database.get_db)
):
    db_detail = await crud.get_point_detail(db, detail_id)
    if db_detail is None:
        raise InternalException(
            "해당 포인트 상세 내역을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return db_detail


@point_router.post(
    "/details",
    response_model=PointDetailSchema,
    summary="포인트 상세 내역 추가",
    description="새로운 포인트 상세 내역을 추가합니다.",
)
async def create_point_detail(
    detail: PointDetailCreate, db: AsyncSession = Depends(database.get_db)
):
    return await crud.create_point_detail(db, detail)


@point_router.put(
    "/details/{detail_id}",
    response_model=PointDetailSchema,
    summary="포인트 상세 내역 수정",
    description="포인트 상세 내역 정보를 수정합니다.",
)
async def update_point_detail(
    detail_id: int,
    detail: PointDetailUpdate,
    db: AsyncSession = Depends(database.get_db),
):
    db_detail = await crud.get_point_detail(db, detail_id)
    if db_detail is None:
        raise InternalException(
            "해당 포인트 상세 내역을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return await crud.update_point_detail(db, detail_id, detail)


@point_router.delete(
    "/details/{detail_id}",
    status_code=204,
    summary="포인트 상세 내역 삭제",
    description="포인트 상세 내역을 삭제합니다.",
)
async def delete_point_detail(
    detail_id: int,
    db: AsyncSession = Depends(database.get_db),
):
    db_detail = await crud.get_point_detail(db, detail_id)
    if db_detail is None:
        raise InternalException(
            "해당 포인트 상세 내역을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    await crud.delete_point_detail(db, detail_id)
    return {"detail": "포인트 상세 내역이 성공적으로 삭제되었습니다."}


# response example : {'user_id': '67a57e83-0078-4f11-af56-286e90469b9a', 'balance': 100}
@point_router.get(
    "/user/{user_id}/balance",
    summary="사용자의 포인트 잔액 조회",
    description="사용자의 포인트 잔액을 조회합니다.",
    dependencies=[Depends(auth)],
)
async def get_user_point_balance(
    request: Request, user_id: str, db: AsyncSession = Depends(database.get_db)
):
    current_user = await check_user(request=request)
    current_user_data = await user_crud.get_user_by_email(
        db=db, user_email=current_user
    )
    if str(current_user_data.id) != user_id:
        raise InternalException(
            "포인트 내역은 본인만 조회할 수 있습니다.", error_code=ErrorCode.FORBIDDEN
        )
    balance = await crud.get_user_points(db, user_id)
    return {"user_id": user_id, "balance": balance}
