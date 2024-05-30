# TODO: 본인이 작성하거나 구매한 여행기만 확인할 수 있도록 수정
# --------------------------------------------------------------------------
# Itinerary model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

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
    "/request",
    response_model=List[ItineraryRequestSchema],
    summary="여행기 요청 전체를 불러오기",
    description="모든 여행기 요청에 대한 정보를 조회합니다.",
)
async def get_all_itinerary_requests(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)
):
    log.info(f"Reading itinerary requests with skip: {skip} and limit: {limit}")
    return await crud.get_all_itinerary_requests(db, skip=skip, limit=limit)


@itinerary_router.get(
    "/request/{request_id}",
    response_model=ItineraryRequestSchema,
    summary="단일 여행기 요청 조회",
    description="단일 여행기 요청에 대한 정보를 조회합니다.",
)
async def read_itinerary_request(
    request_id: str, db: AsyncSession = Depends(database.get_db)
):
    db_itinerary_request = await crud.get_itinerary_request(db, request_id)
    if db_itinerary_request is None:
        raise InternalException(
            "해당 여행기 요청을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return db_itinerary_request


@itinerary_router.post(
    "/request",
    response_model=ItineraryRequestSchema,
    summary="여행기 요청 추가",
    description="새로운 여행기 요청을 추가합니다.",
)
async def create_itinerary_request(
    itinerary_request: ItineraryRequestCreate,
    db: AsyncSession = Depends(database.get_db),
):
    return await crud.create_itinerary_request(db, itinerary_request)


@itinerary_router.put(
    "/request/{request_id}",
    response_model=ItineraryRequestSchema,
    summary="여행기 요청 정보 수정",
    description="여행기 요청 정보를 수정합니다.",
)
async def update_itinerary_request(
    request_id: str,
    itinerary_request: ItineraryRequestUpdate,
    db: AsyncSession = Depends(database.get_db),
):
    db_itinerary_request = await crud.get_itinerary_request(db, request_id)
    if db_itinerary_request is None:
        raise InternalException(
            "해당 여행기 요청을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return await crud.update_itinerary_request(db, request_id, itinerary_request)


@itinerary_router.delete(
    "/request/{request_id}",
    status_code=204,
    summary="여행기 요청 삭제",
    description="여행기 요청을 삭제합니다.",
)
async def delete_itinerary_request(
    request_id: str,
    db: AsyncSession = Depends(database.get_db),
):
    db_itinerary_request = await crud.get_itinerary_request(db, request_id)
    if db_itinerary_request is None:
        raise InternalException(
            "해당 여행기 요청을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    await crud.delete_itinerary_request(db, request_id)
    return {"detail": "여행기 요청이 성공적으로 삭제되었습니다."}


@itinerary_router.get(
    "/",
    response_model=List[ItinerarySchema],
    summary="여행기 전체를 불러오기",
    description="모든 여행기에 대한 정보를 조회합니다.",
)
async def get_all_itineraries(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)
):
    log.info(f"Reading itineraries with skip: {skip} and limit: {limit}")
    return await crud.get_all_itineraries(db, skip=skip, limit=limit)


@itinerary_router.get(
    "/{itinerary_id}",
    response_model=ItinerarySchema,
    summary="단일 여행기 조회",
    description="단일 여행기에 대한 정보를 조회합니다.",
)
async def read_itinerary(
    itinerary_id: str, db: AsyncSession = Depends(database.get_db)
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
