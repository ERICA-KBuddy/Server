# --------------------------------------------------------------------------
# Area model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import httpx

from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import area as crud
from src.db import database
from src.schemas.requests import (
    AreaCreate,
    AreaUpdate,
    AreaImageCreate,
    AreaImageUpdate,
)
from src.db.data import csv_converter
from src.core.settings import settings
from src.schemas.responses import AreaSchema, AreaImageSchema, AreaSchemaAPI
from src.helper.exceptions import InternalException, ErrorCode


log = getLogger(__name__)
area_router = APIRouter(prefix="/area")


async def get_area_data():
    file_path = "src/db/data/20240602001629_지역별 방문자 수.csv"
    random_area = await csv_converter.get_random_area(file_path)

    # 지역 코드 정보를 조회하는 API 요청
    area_code_url = f"{settings.TOUR_API_ENDPOINT}/areaCode1"
    area_code_params = {
        "serviceKey": settings.TOUR_API_KEY_DECODING,
        "numOfRows": 30,
        "pageNo": 1,
        "MobileOS": "ETC",
        "MobileApp": "K-Buddy",
        "_type": "JSON",
        "areaCode": 1
    }

    async with httpx.AsyncClient() as client:
        area_code_response = await client.get(area_code_url, params=area_code_params)
        if area_code_response.status_code != 200:
            raise HTTPException(status_code=area_code_response.status_code, detail="Failed to fetch area codes")

        area_codes = area_code_response.json()
        area_code = None
        for item in area_codes['response']['body']['items']['item']:
            if item['name'] == random_area:
                area_code = item['code']
                break

        if not area_code:
            raise HTTPException(status_code=404, detail="Area code not found for selected area")

        # 관광 정보 조회하는 API 요청
        tour_info_url = f"{settings.TOUR_API_ENDPOINT}/areaBasedList1"
        tour_info_params = {
            "serviceKey": settings.TOUR_API_KEY_DECODING,
            "numOfRows": 5,
            "pageNo": 1,
            "MobileOS": "ETC",
            "MobileApp": "K-Buddy",
            "listYN": "Y",
            "arrange": "A",
            "areaCode": 1,
            "sigunguCode": area_code,
            "_type": "JSON",
        }

        tour_info_response = await client.get(tour_info_url, params=tour_info_params)
        if tour_info_response.status_code != 200:
            raise HTTPException(status_code=tour_info_response.status_code, detail="Failed to fetch tour info")

        tour_info = tour_info_response.json()

    return tour_info


@area_router.get(
    "/curate",
    response_model=List[AreaSchemaAPI],
    summary="지역 큐레이션",
    description="사용자에게 최근 가장 트랜드한 장소 5개를 큐레이션합니다."
)
async def cureate_areas(

):
    tour_info = await get_area_data()

    areas = []
    for item in tour_info['response']['body']['items']['item']:
        area = AreaSchemaAPI(
            name=item.get('title', ''),
            address=item.get('addr1', ''),
            website=item.get('homepage', None),
            contact_num=item.get('tel', None),
            open_time=item.get('usetime', None),
            image=item.get('firstimage', '')
        )
        areas.append(area)

    return areas


@area_router.get(
    "/list",
    response_model=List[AreaSchema],
    summary="지역 전체를 불러오기",
    description="모든 지역에 대한 정보를 조회합니다.",
)
async def get_all_areas(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)
):
    log.info(f"Reading students info with skip: {skip} and limit: {limit}")
    return await crud.get_all_areas(db, skip=skip, limit=limit)


@area_router.get(
    "/{area_id}",
    response_model=AreaSchema,
    summary="단일 지역 조회",
    description="하나의 지역에 대한 정보를 조회합니다.",
)
async def read_area(area_id: int, db: AsyncSession = Depends(database.get_db)):
    db_area = await crud.get_area(db, area_id)
    if db_area is None:
        raise InternalException(
            "해당 지역을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return db_area


@area_router.post(
    "/add",
    response_model=AreaSchema,
    summary="단일 지역 추가",
    description="새로운 지역 정보를 데이터베이스에 추가합니다.",
)
async def create_area(area: AreaCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_area(db, area)


@area_router.put(
    "/{area_id}",
    response_model=AreaSchema,
    summary="단일 지역 정보 수정",
    description="지역 정보를 수정합니다.",
)
async def update_area(
    area_id: int,
    area: AreaUpdate,
    db: AsyncSession = Depends(database.get_db),
):
    return await crud.update_area(db, area_id, area)


@area_router.delete(
    "/{area_id}",
    status_code=204,
    summary="단일 지역 삭제",
    description="지역을 삭제합니다.",
)
async def delete_area(
    area_id: int,
    db: AsyncSession = Depends(database.get_db),
):
    await crud.delete_area(db, area_id)
    return {"detail": "지역이 성공적으로 삭제되었습니다."}


@area_router.get(
    "/{area_id}/images",
    response_model=List[AreaImageSchema],
    summary="지역 이미지 조회",
    description="지역에 해당하는 모든 이미지를 조회합니다.",
)
async def get_area_images(
    area_id: int,
    db: AsyncSession = Depends(database.get_db),
    skip: int = 0,
    limit: int = 100,
):
    db_area = await crud.get_area(db, area_id)
    if db_area is None:
        raise InternalException(
            "해당 지역을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return await crud.get_area_images(db, area_id, skip=skip, limit=limit)


@area_router.get(
    "/images/{image_id}",
    response_model=AreaImageSchema,
    summary="단일 지역 이미지 조회",
    description="단일 지역 이미지를 조회합니다.",
)
async def get_area_image(image_id: int, db: AsyncSession = Depends(database.get_db)):
    db_image = await crud.get_area_image(db, image_id)
    if db_image is None:
        raise InternalException(
            "해당 지역의 이미지를 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return db_image


@area_router.post(
    "/{area_id}/images",
    response_model=AreaImageSchema,
    summary="지역 이미지 추가",
    description="지역에 새로운 이미지를 추가합니다.",
)
async def create_area_image(
    area_id: int, image: AreaImageCreate, db: AsyncSession = Depends(database.get_db)
):
    db_area = await crud.get_area(db, area_id)
    if db_area is None:
        raise InternalException(
            "해당 지역을 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return await crud.create_area_image(db, area_id, image)


@area_router.put(
    "/images/{image_id}",
    response_model=AreaImageSchema,
    summary="지역 이미지 수정",
    description="지역 이미지를 수정합니다.",
)
async def update_area_image(
    image_id: int, image: AreaImageUpdate, db: AsyncSession = Depends(database.get_db)
):
    db_image = await crud.get_area_image(db, image_id)
    if db_image is None:
        raise InternalException(
            "해당 이미지를 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    return await crud.update_area_image(db, image_id, image)


@area_router.delete(
    "/images/{image_id}",
    status_code=204,
    summary="지역 이미지 삭제",
    description="지역의 이미지를 삭제합니다.",
)
async def delete_area_image(image_id: int, db: AsyncSession = Depends(database.get_db)):
    db_image = await crud.get_area_image(db, image_id)
    if db_image is None:
        raise InternalException(
            "해당 이미지를 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND
        )
    await crud.delete_area_image(db, image_id)
    return {"detail": "이미지가 성공적으로 삭제되었습니다."}
