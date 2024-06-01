# TODO: itinerary_router CREATE 메서드 로직 수정
# --------------------------------------------------------------------------
# Itinerary model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.router._check import check_user, auth, get_current_user_info
from src.crud import itinerary as crud
from src.db import database
from src.helper.exceptions import InternalException, ErrorCode
from src.schemas.requests import (
    ItineraryRequestUpdate,
    ItineraryRequestCreate,
    ItineraryCreate,
)
from src.schemas.responses import ItinerarySchema, ItineraryRequestSchema


log = getLogger(__name__)
itinerary_router = APIRouter(prefix="/itinerary")


@itinerary_router.get(
    "/request/",
    response_model=List[ItineraryRequestSchema],
    summary="여행기 요청 전체를 불러오기",
    description="본인이 작성한 모든 여행기 요청에 대한 정보를 조회합니다.",
    dependencies=[Depends(auth)],
)
async def get_all_itinerary_requests(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(database.get_db),
):
    current_user = await get_current_user_info(request, db)
    log.info(f"Reading itinerary requests with skip: {skip} and limit: {limit}")
    return await crud.get_all_itinerary_requests(
        db, str(current_user.id), skip=skip, limit=limit
    )


@itinerary_router.get(
    "/request/{request_id}",
    response_model=ItineraryRequestSchema,
    summary="단일 여행기 요청 조회",
    description="단일 여행기 요청에 대한 정보를 조회합니다.",
    dependencies=[Depends(auth)],
)
async def read_itinerary_request(
    request: Request, request_id: str, db: AsyncSession = Depends(database.get_db)
):
    current_user = await get_current_user_info(request, db)
    db_itinerary_request = await crud.get_itinerary_request(db, request_id)
    if db_itinerary_request is None:
        raise InternalException(
            "해당 여행기 요청을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    if db_itinerary_request.request_user_id != current_user.id:
        raise InternalException(
            "본인이 작성한 여행기 요청서만 볼 수 있습니다.",
            error_code=ErrorCode.FORBIDDEN,
        )
    return db_itinerary_request


@itinerary_router.post(
    "/request/",
    response_model=ItineraryRequestSchema,
    summary="여행기 요청 추가",
    description="새로운 여행기 요청을 추가합니다.",
    dependencies=[Depends(auth)],
)
async def create_itinerary_request(
    request: Request,
    itinerary_request: ItineraryRequestCreate,
    db: AsyncSession = Depends(database.get_db),
):
    current_user = await get_current_user_info(request, db)
    itinerary_request.request_user_id = current_user.id
    return await crud.create_itinerary_request(db, itinerary_request)


@itinerary_router.put(
    "/request/{request_id}",
    response_model=ItineraryRequestSchema,
    summary="여행기 요청 정보 수정",
    description="여행기 요청 정보를 수정합니다.",
    dependencies=[Depends(auth)],
)
async def update_itinerary_request(
    request: Request,
    request_id: str,
    itinerary_request: ItineraryRequestUpdate,
    db: AsyncSession = Depends(database.get_db),
):
    current_user = await get_current_user_info(request, db)
    db_itinerary_request = await crud.get_itinerary_request(db, request_id)
    if db_itinerary_request is None:
        raise InternalException(
            "해당 여행기 요청을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    if db_itinerary_request.request_user_id != current_user.id:
        raise InternalException(
            "본인이 작성한 여행기 요청서만 수정할 수 있습니다.",
            error_code=ErrorCode.FORBIDDEN,
        )
    return await crud.update_itinerary_request(db, request_id, itinerary_request)


@itinerary_router.post(
    "/request/{request_id}/delete",
    status_code=204,
    summary="단일 여행기 요청 삭제",
    description="여행기 요청을 삭제합니다.",
    dependencies=[Depends(auth)],
)
async def delete_itinerary_request(
    request: Request,
    request_id: str,
    db: AsyncSession = Depends(database.get_db),
):
    current_user = await get_current_user_info(request, db)
    db_itinerary_request = await crud.get_itinerary_request(db, request_id)
    if db_itinerary_request is None:
        raise InternalException(
            "해당 여행기 요청을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    if db_itinerary_request.request_user_id != current_user.id:
        raise InternalException(
            "본인이 작성한 여행기 요청서만 삭제할 수 있습니다.",
            error_code=ErrorCode.FORBIDDEN,
        )
    deleted_id = await crud.delete_itinerary_request(db, request_id)
    return {"detail": "여행기 요청이 성공적으로 삭제되었습니다."}


@itinerary_router.get(
    "/{itinerary_id}",
    response_model=ItinerarySchema,
    summary="단일 여행기 조회",
    description="단일 여행기에 대한 정보를 조회합니다.",
)
async def read_itinerary(
    request: Request, itinerary_id: str, db: AsyncSession = Depends(database.get_db)
):
    db_itinerary = await crud.get_itinerary(db, itinerary_id)
    if db_itinerary is None:
        raise InternalException(
            "해당 여행기를 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )

    return db_itinerary


@itinerary_router.post(
    "/",
    response_model=ItinerarySchema,
    summary="여행기 추가",
    description="새로운 여행기를 추가합니다.",
)
async def create_itinerary(
    itinerary: ItineraryCreate, db: AsyncSession = Depends(database.get_db)
):
    return await crud.create_itinerary(db, itinerary)


@itinerary_router.delete(
    "/{itinerary_id}",
    status_code=204,
    summary="여행기 삭제",
    description="여행기를 삭제합니다.",
)
async def delete_itinerary(
    itinerary_id: str,
    db: AsyncSession = Depends(database.get_db),
):
    db_itinerary = await crud.get_itinerary(db, itinerary_id)
    if db_itinerary is None:
        raise InternalException(
            "해당 여행기를 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    await crud.delete_itinerary(db, itinerary_id)
    return {"detail": "여행기가 성공적으로 삭제되었습니다."}
