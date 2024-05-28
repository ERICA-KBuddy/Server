# --------------------------------------------------------------------------
# User model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
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
from src.db.models import User
from src.schemas.requests import UserCreate, UserUpdate
from src.schemas.responses import UserSchema
from src.helper.exceptions import InternalException, ErrorCode
from src.utils.authentication import decode_user_data_from_token, get_password_hash


async def get_all_users(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[UserSchema]:
    return await get_objects(
        db=db,
        model=User,
        response_model=UserSchema,
        # condition="",
        skip=skip,
        limit=limit,
    )


async def get_user(db: AsyncSession, user_uid: str) -> Optional[UserSchema]:
    return await get_object(
        db=db, model=User, model_id=user_uid, response_model=UserSchema
    )


async def get_user_by_email(db: AsyncSession, user_email: str) -> Optional[UserSchema]:
    result = await db.execute(select(User).where(User.email == user_email))
    return result.scalars().first()


async def get_current_user(db: AsyncSession):
    _, user_email = decode_user_data_from_token()
    user = await get_user_by_email(user_email=user_email, db=db)
    if user is None:
        raise InternalException(
            "데이터베이스에 해당 유저 정보가 없습니다.",
            error_code=ErrorCode.UNAUTHORIZED,
        )
    return user


async def create_user(db: AsyncSession, user: UserCreate) -> UserSchema:
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    return await create_object(db=db, model=User, obj=user, response_model=UserSchema)


async def update_user(
    db: AsyncSession, user_id: str, user: UserUpdate
) -> Optional[UserSchema]:
    return await update_object(
        db=db,
        model=User,
        model_id=user_id,
        obj=user,
        response_model=UserSchema,
    )


async def delete_user(db: AsyncSession, user_id: str) -> Optional[int]:
    return await delete_object(db=db, model=User, model_id=user_id)


async def get_user_by_identifier(db: AsyncSession, identifier: str) -> Optional[User]:
    query = select(User).filter(
        (User.email == identifier) | (User.nickname == identifier)
    )
    db_obj = (await db.execute(query)).scalar_one()

    return db_obj
