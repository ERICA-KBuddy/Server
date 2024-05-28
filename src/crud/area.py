# --------------------------------------------------------------------------
# Area model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
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
from src.db.models import Area, AreaImage
from src.schemas.responses import AreaSchema, AreaImageSchema
from src.schemas.requests import (
    AreaCreate,
    AreaUpdate,
    AreaImageCreate,
    AreaImageUpdate,
)


async def get_all_areas(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[AreaSchema]:
    return await get_objects(
        db=db,
        model=Area,
        response_model=AreaSchema,
        # condition="",
        skip=skip,
        limit=limit,
    )


async def get_area(db: AsyncSession, area_id: int) -> Optional[AreaSchema]:
    return await get_object(
        db=db, model=Area, model_id=area_id, response_model=AreaSchema
    )


async def create_area(db: AsyncSession, area: AreaCreate) -> AreaSchema:
    return await create_object(db=db, model=Area, obj=area, response_model=AreaSchema)


async def update_area(
    db: AsyncSession, area_id: int, area: AreaUpdate
) -> Optional[AreaSchema]:
    return await update_object(
        db=db,
        model=Area,
        model_id=area_id,
        obj=area,
        response_model=AreaSchema,
    )


async def delete_area(db: AsyncSession, area_id: int) -> Optional[int]:
    return await delete_object(db=db, model=Area, model_id=area_id)


async def get_area_images(
    db: AsyncSession, area_id: int, skip: int = 0, limit: int = 100
) -> List[AreaImageSchema]:
    condition = AreaImage.area_id == area_id
    return await get_objects(
        db=db,
        model=AreaImage,
        response_model=AreaImageSchema,
        condition=condition,
        skip=skip,
        limit=limit,
    )


async def get_area_image(db: AsyncSession, image_id: int) -> Optional[AreaImageSchema]:
    return await get_object(
        db=db, model=AreaImage, model_id=image_id, response_model=AreaImageSchema
    )


async def create_area_image(
    db: AsyncSession, area_id: int, image: AreaImageCreate
) -> AreaImageSchema:
    db_image = AreaImage(area_id=area_id, **image.model_dump())
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)
    return AreaImageSchema.model_validate(db_image)


async def update_area_image(
    db: AsyncSession, image_id: int, image: AreaImageUpdate
) -> Optional[AreaImageSchema]:
    return await update_object(
        db=db,
        model=AreaImage,
        model_id=image_id,
        obj=image,
        response_model=AreaImageSchema,
    )


async def delete_area_image(db: AsyncSession, image_id: int) -> Optional[int]:
    return await delete_object(db=db, model=AreaImage, model_id=image_id)
