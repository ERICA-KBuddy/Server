# --------------------------------------------------------------------------
# Point model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
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
    update_object,
    delete_object,
)
from src.db.models import PointDetail, PointEvent
from src.schemas.requests import (
    PointEventCreate,
    PointEventUpdate,
    PointDetailCreate,
    PointDetailUpdate,
)
from src.schemas.responses import PointDetailSchema, PointEventSchema


async def get_all_point_events(
    db: AsyncSession, target_user: str, skip: int = 0, limit: int = 100
) -> List[PointEventSchema]:
    condition = f"user_id='{target_user}'"
    return await get_objects(
        db=db,
        condition=condition,
        model=PointEvent,
        response_model=PointEventSchema,
        skip=skip,
        limit=limit,
    )


async def get_point_event(
    db: AsyncSession, event_id: int
) -> Optional[PointEventSchema]:
    return await get_object(
        db=db, model=PointEvent, model_id=event_id, response_model=PointEventSchema
    )


async def create_point_event(
    db: AsyncSession, event: PointEventCreate
) -> PointEventSchema:
    return await create_object(
        db=db, model=PointEvent, obj=event, response_model=PointEventSchema
    )


async def update_point_event(
    db: AsyncSession, event_id: int, event: PointEventUpdate
) -> Optional[PointEventSchema]:
    return await update_object(
        db=db,
        model=PointEvent,
        model_id=event_id,
        obj=event,
        response_model=PointEventSchema,
    )


async def delete_point_event(db: AsyncSession, event_id: int) -> Optional[int]:
    return await delete_object(db=db, model=PointEvent, model_id=event_id)


async def get_all_point_details(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[PointDetailSchema]:
    return await get_objects(
        db=db,
        model=PointDetail,
        response_model=PointDetailSchema,
        skip=skip,
        limit=limit,
    )


async def get_point_detail(
    db: AsyncSession, detail_id: int
) -> Optional[PointDetailSchema]:
    return await get_object(
        db=db, model=PointDetail, model_id=detail_id, response_model=PointDetailSchema
    )


async def create_point_detail(
    db: AsyncSession, detail: PointDetailCreate
) -> PointDetailSchema:
    return await create_object(
        db=db, model=PointDetail, obj=detail, response_model=PointDetailSchema
    )


async def update_point_detail(
    db: AsyncSession, detail_id: int, detail: PointDetailUpdate
) -> Optional[PointDetailSchema]:
    return await update_object(
        db=db,
        model=PointDetail,
        model_id=detail_id,
        obj=detail,
        response_model=PointDetailSchema,
    )


async def delete_point_detail(db: AsyncSession, detail_id: int) -> Optional[int]:
    return await delete_object(db=db, model=PointDetail, model_id=detail_id)


# Function to calculate remaining points
async def get_user_points(db: AsyncSession, user_id: str) -> int:
    query = select(PointEvent).where(PointEvent.user_id == user_id)
    result = await db.execute(query)
    events = result.scalars().all()

    total_points = 0
    for event in events:
        total_points += event.amount

    query = select(PointDetail).where(PointDetail.event_id.in_([e.id for e in events]))
    result = await db.execute(query)
    details = result.scalars().all()

    for detail in details:
        total_points -= detail.point

    return total_points
