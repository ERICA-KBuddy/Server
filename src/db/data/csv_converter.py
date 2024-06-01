import chardet
import pandas as pd

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Area
from src.db import database
from src.schemas.requests import AreaCreate


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


if __name__ == "__main__":
    import asyncio

    async def main():
        async with database.get_db() as db:
            await csv_to_db(db)


    asyncio.run(main())
