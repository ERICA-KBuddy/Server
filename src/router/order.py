# --------------------------------------------------------------------------
# Order model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import order as crud
from src.db import database
from src.helper.exceptions import InternalException, ErrorCode
from src.schemas.requests import OrderCreate, OrderUpdate
from src.schemas.responses import OrderSchema


log = getLogger(__name__)
order_router = APIRouter(prefix="/order")


@order_router.get(
    "/",
    response_model=List[OrderSchema],
    summary="주문 전체를 불러오기",
    description="모든 주문에 대한 정보를 조회합니다.",
)
async def get_all_orders(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)
):
    log.info(f"Reading orders with skip: {skip} and limit: {limit}")
    return await crud.get_all_orders(db, skip=skip, limit=limit)


@order_router.get(
    "/{order_id}",
    response_model=OrderSchema,
    summary="단일 주문 조회",
    description="단일 주문에 대한 정보를 조회합니다.",
)
async def read_order(order_id: str, db: AsyncSession = Depends(database.get_db)):
    db_order = await crud.get_order(db, order_id)
    if db_order is None:
        raise InternalException(
            "해당 주문을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return db_order


@order_router.post(
    "/",
    response_model=OrderSchema,
    summary="주문 추가",
    description="새로운 주문을 추가합니다.",
)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_order(db, order)


@order_router.put(
    "/{order_id}",
    response_model=OrderSchema,
    summary="주문 정보 수정",
    description="주문 정보를 수정합니다.",
)
async def update_order(
    order_id: str,
    order: OrderUpdate,
    db: AsyncSession = Depends(database.get_db),
):
    db_order = await crud.get_order(db, order_id)
    if db_order is None:
        raise InternalException(
            "해당 주문을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return await crud.update_order(db, order_id, order)


@order_router.delete(
    "/{order_id}",
    status_code=204,
    summary="주문 삭제",
    description="주문을 삭제합니다.",
)
async def delete_order(
    order_id: str,
    db: AsyncSession = Depends(database.get_db),
):
    db_order = await crud.get_order(db, order_id)
    if db_order is None:
        raise InternalException(
            "해당 주문을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    await crud.delete_order(db, order_id)
    return {"detail": "주문이 성공적으로 삭제되었습니다."}
