import random
import chardet
import pandas as pd

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Area
from src.db import database
from src.schemas.requests import AreaCreate
from enum import Enum


class AreaName(Enum):
    강남구 = "Gangnam-gu"
    강동구 = "Gangdong-gu"
    강북구 = "Gangbuk-gu"
    강서구 = "Gangseo-gu"
    관악구 = "Gwanak-gu"
    광진구 = "Gwangjin-gu"
    구로구 = "Guro-gu"
    금천구 = "Geumcheon-gu"
    노원구 = "Nowon-gu"
    도봉구 = "Dobong-gu"
    동대문구 = "Dongdaemun-gu"
    동작구 = "Dongjak-gu"
    마포구 = "Mapo-gu"
    서대문구 = "Seodaemun-gu"
    서초구 = "Seocho-gu"
    성동구 = "Seongdong-gu"
    성북구 = "Seongbuk-gu"
    송파구 = "Songpa-gu"
    양천구 = "Yangcheon-gu"
    영등포구 = "Yeongdeungpo-gu"
    용산구 = "Yongsan-gu"
    은평구 = "Eunpyeong-gu"
    종로구 = "Jongno-gu"
    중구 = "Jung-gu"
    중랑구 = "Jungnang-gu"


async def create_data(db: AsyncSession, data: AreaCreate):
    db_data = Area(**data.model_dump())
    db.add(db_data)
    await db.commit()
    await db.refresh(db_data)
    return db_data


def detect_encoding(file_path: str) -> str:
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


async def csv_to_db(db: AsyncSession):
    file_path = "src/db/data/한국문화관광연구원_관광자원정보.csv"
    encoding = detect_encoding(file_path)

    df = pd.read_csv(file_path, encoding=encoding)
    df = df.dropna(subset=['영문명'])
    df['영문명'] = df['영문명'].str.strip()
    df = df.drop_duplicates(subset=['영문명'])

    for _, row in df.iterrows():
        data = AreaCreate(
            name=str(row['영문명']),
            address=str(row['상세주소']),
            website=str(row['홈페이지']),
            contact_num=str(row['연락처']),
        )
        await create_data(db, data)


async def get_top_5_areas(file_path: str):
    encoding = detect_encoding(file_path)
    df = pd.read_csv(file_path, encoding=encoding)

    df['기초지자체명'] = df['기초지자체명'].str.strip()

    df = df.dropna(subset=['기초지자체 방문자 수'])

    top_5_areas = df.sort_values(by='기초지자체 방문자 수', ascending=False).head(5)

    top_5_areas['기초지자체명_영어'] = top_5_areas['기초지자체명'].map(
        lambda x: AreaName[x].value if x in AreaName.__members__ else x)

    return top_5_areas['기초지자체명_영어'].tolist()


async def get_random_area(file_path: str):
    top_5_areas = await get_top_5_areas(file_path)
    return random.choice(top_5_areas)


if __name__ == "__main__":
    import asyncio

    async def main():
        async with database.get_db() as db:
            await csv_to_db(db)


    asyncio.run(main())
