# --------------------------------------------------------------------------
# Itinerary model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
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
from src.db.models import Itinerary, ItineraryRequest
from src.schemas.requests import (
    ItineraryRequestCreate,
    ItineraryRequestUpdate,
    ItineraryCreate,
)
from src.schemas.responses import ItinerarySchema, ItineraryRequestSchema


async def get_all_itinerary_requests(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[ItineraryRequestSchema]:
    return await get_objects(
        db=db,
        model=ItineraryRequest,
        response_model=ItineraryRequestSchema,
        skip=skip,
        limit=limit,
    )


async def get_itinerary_request(
    db: AsyncSession, request_id: str
) -> Optional[ItineraryRequestSchema]:
    return await get_object(
        db=db,
        model=ItineraryRequest,
        model_id=request_id,
        response_model=ItineraryRequestSchema,
    )


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
    return await update_object(
        db=db,
        model=ItineraryRequest,
        model_id=request_id,
        obj=request,
        response_model=ItineraryRequestSchema,
    )


async def delete_itinerary_request(db: AsyncSession, request_id: str) -> Optional[int]:
    return await delete_object(db=db, model=ItineraryRequest, model_id=request_id)


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
