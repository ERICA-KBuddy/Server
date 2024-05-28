# --------------------------------------------------------------------------
# Order model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
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
from src.db.models import Order
from src.schemas.requests import OrderCreate, OrderUpdate
from src.schemas.responses import OrderSchema


async def get_all_orders(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[OrderSchema]:
    return await get_objects(
        db=db,
        model=Order,
        response_model=OrderSchema,
        skip=skip,
        limit=limit,
    )


async def get_order(db: AsyncSession, order_id: str) -> Optional[OrderSchema]:
    return await get_object(
        db=db, model=Order, model_id=order_id, response_model=OrderSchema
    )


async def create_order(db: AsyncSession, order: OrderCreate) -> OrderSchema:
    return await create_object(
        db=db, model=Order, obj=order, response_model=OrderSchema
    )


async def update_order(
    db: AsyncSession, order_id: str, order: OrderUpdate
) -> Optional[OrderSchema]:
    return await update_object(
        db=db,
        model=Order,
        model_id=order_id,
        obj=order,
        response_model=OrderSchema,
    )


async def delete_order(db: AsyncSession, order_id: str) -> Optional[int]:
    return await delete_object(db=db, model=Order, model_id=order_id)
