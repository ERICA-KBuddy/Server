# --------------------------------------------------------------------------
# Listing model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import listing as crud
from src.db import database
from src.helper.exceptions import InternalException, ErrorCode
from src.schemas.requests import ListingCreate, ListingUpdate
from src.schemas.responses import ListingSchema


log = getLogger(__name__)
listing_router = APIRouter(prefix="/listing")


@listing_router.get(
    "/",
    response_model=List[ListingSchema],
    summary="판매글 전체를 불러오기",
    description="모든 판매글을 조회합니다.",
)
async def get_all_listings(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)
):
    log.info(f"Reading listings with skip: {skip} and limit: {limit}")
    return await crud.get_all_listings(db, skip=skip, limit=limit)


@listing_router.get(
    "/{listing_id}",
    response_model=ListingSchema,
    summary="단일 판매글 조회",
    description="단일 판매글에 대한 정보를 조회합니다.",
)
async def read_listing(listing_id: str, db: AsyncSession = Depends(database.get_db)):
    db_listing = await crud.get_listing(db, listing_id)
    if db_listing is None:
        raise InternalException(
            "해당 판매글을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return db_listing


@listing_router.post(
    "/",
    response_model=ListingSchema,
    summary="판매글 추가",
    description="새로운 판매글 추가합니다.",
)
async def create_listing(
    listing: ListingCreate, db: AsyncSession = Depends(database.get_db)
):
    return await crud.create_listing(db, listing)


@listing_router.put(
    "/{listing_id}",
    response_model=ListingSchema,
    summary="판매글 정보 수정",
    description="판매글 정보를 수정합니다.",
)
async def update_listing(
    listing_id: str,
    listing: ListingUpdate,
    db: AsyncSession = Depends(database.get_db),
):
    db_listing = await crud.get_listing(db, listing_id)
    if db_listing is None:
        raise InternalException(
            "해당 판매글을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return await crud.update_listing(db, listing_id, listing)


@listing_router.delete(
    "/{listing_id}",
    status_code=204,
    summary="판매글 삭제",
    description="판매글을 삭제합니다.",
)
async def delete_listing(
    listing_id: str,
    db: AsyncSession = Depends(database.get_db),
):
    db_listing = await crud.get_listing(db, listing_id)
    if db_listing is None:
        raise InternalException(
            "해당 판매글을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    await crud.delete_listing(db, listing_id)
    return {"detail": "판매글이 성공적으로 삭제되었습니다."}
