# --------------------------------------------------------------------------
# Listing model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from __future__ import annotations

from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ._base import (
    get_objects,
    get_object,
    create_object,
    update_object,
    delete_object,
)
from src.db.models import Listing
from src.schemas.requests import ListingCreate, ListingUpdate
from src.schemas.responses import ListingSchema


async def get_all_listings(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[ListingSchema]:
    return await get_objects(
        db=db,
        model=Listing,
        response_model=ListingSchema,
        skip=skip,
        limit=limit,
    )


async def get_listing(db: AsyncSession, listing_id: str) -> Optional[ListingSchema]:
    return await get_object(
        db=db, model=Listing, model_id=listing_id, response_model=ListingSchema
    )


async def create_listing(db: AsyncSession, listing: ListingCreate) -> ListingSchema:
    return await create_object(
        db=db, model=Listing, obj=listing, response_model=ListingSchema
    )


async def update_listing(
    db: AsyncSession, listing_id: str, listing: ListingUpdate
) -> Optional[ListingSchema]:
    return await update_object(
        db=db,
        model=Listing,
        model_id=listing_id,
        obj=listing,
        response_model=ListingSchema,
    )


async def delete_listing(db: AsyncSession, listing_id: str) -> Optional[int]:
    return await delete_object(db=db, model=Listing, model_id=listing_id)
