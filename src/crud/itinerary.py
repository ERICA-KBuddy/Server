# --------------------------------------------------------------------------
# Itinerary model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ._base import (
    get_objects,
    get_object,
    create_object,
    delete_object,
)
from src.db.models import Itinerary, ItineraryRequest
from src.schemas.requests import (
    ItineraryRequestCreate,
    ItineraryRequestUpdate,
    ItineraryCreate,
)
from src.schemas.responses import ItinerarySchema, ItineraryRequestSchema


async def get_all_itinerary_requests(
    db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100
) -> List[ItineraryRequestSchema]:
    query = (
        select(ItineraryRequest)
        .where(ItineraryRequest.is_deleted == False)
        .where(ItineraryRequest.request_user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    return [
        ItineraryRequestSchema.model_validate(item) for item in result.scalars().all()
    ]


async def get_itinerary_request(
    db: AsyncSession, request_id: str
) -> Optional[ItineraryRequestSchema]:
    result = await db.get(ItineraryRequest, request_id)
    if result and not result.is_deleted:
        return ItineraryRequestSchema.model_validate(result)
    return None


async def create_itinerary_request(
    db: AsyncSession, request: ItineraryRequestCreate
) -> ItineraryRequestSchema:
    return await create_object(
        db=db,
        model=ItineraryRequest,
        obj=request,
        response_model=ItineraryRequestSchema,
    )


async def update_itinerary_request(
    db: AsyncSession, request_id: str, request: ItineraryRequestUpdate
) -> Optional[ItineraryRequestSchema]:
    db_itinerary_request = await db.get(ItineraryRequest, request_id)
    if db_itinerary_request is None or db_itinerary_request.is_deleted:
        return None
    for key, value in request.model_dump(exclude_unset=True).items():
        setattr(db_itinerary_request, key, value)
    db.add(db_itinerary_request)
    await db.commit()
    await db.refresh(db_itinerary_request)
    return ItineraryRequestSchema.model_validate(db_itinerary_request)


async def delete_itinerary_request(db: AsyncSession, request_id: str) -> Optional[str]:
    db_itinerary_request = await db.get(ItineraryRequest, request_id)
    db_itinerary_request.is_deleted = True
    db.add(db_itinerary_request)
    await db.commit()
    return request_id


async def get_all_itineraries(
    db: AsyncSession, target_user: str, skip: int = 0, limit: int = 100
) -> List[ItinerarySchema]:
    condition = f"user_id='{target_user}'"
    return await get_objects(
        db=db,
        condition=condition,
        model=Itinerary,
        response_model=ItinerarySchema,
        skip=skip,
        limit=limit,
    )


async def get_itinerary(
    db: AsyncSession, itinerary_id: str
) -> Optional[ItinerarySchema]:
    return await get_object(
        db=db, model=Itinerary, model_id=itinerary_id, response_model=ItinerarySchema
    )


async def create_itinerary(
    db: AsyncSession, itinerary: ItineraryCreate
) -> ItinerarySchema:
    return await create_object(
        db=db, model=Itinerary, obj=itinerary, response_model=ItinerarySchema
    )


async def delete_itinerary(db: AsyncSession, itinerary_id: str) -> Optional[int]:
    return await delete_object(db=db, model=Itinerary, model_id=itinerary_id)
