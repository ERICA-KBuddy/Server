# --------------------------------------------------------------------------
# Item model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Item
from src.crud._base import (
    create_object,
    get_object,
    get_objects,
    delete_object,
    update_object,
)
from src.schemas import item as schema


async def create_item(db: AsyncSession, item: schema.ItemCreate) -> schema.Item:
    return await create_object(db=db, model=Item, obj=item, response_model=schema.Item)


async def get_item(db: AsyncSession, item_id: int) -> Optional[schema.Item]:
    return await get_object(
        db=db, model=Item, model_id=item_id, response_model=schema.Item
    )


async def get_items(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[schema.Item]:
    return await get_objects(
        db=db, model=Item, response_model=schema.Item, skip=skip, limit=limit
    )


async def update_item(
    db: AsyncSession, item_id: int, item: schema.ItemUpdate
) -> Optional[schema.Item]:
    return await update_object(
        db=db, model=Item, model_id=item_id, obj=item, response_model=schema.Item
    )


async def delete_item(db: AsyncSession, item_id: int) -> Optional[int]:
    return await delete_object(db=db, model=Item, model_id=item_id)
