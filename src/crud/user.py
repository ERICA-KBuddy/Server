# --------------------------------------------------------------------------
# User model의 CRUD를 담당하는 메서드를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ._base import get_objects, get_object, create_object, update_object, delete_object
from src.db.models import User

from src.schemas.requests import UserCreate, UserUpdate
from src.schemas.responses import UserSchema


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


async def get_user(db, user_id) -> Optional[UserSchema]:
    return await get_object(
        db=db, model=User, model_id=user_id, response_model=UserSchema
    )


async def create_user(db: AsyncSession, user: UserCreate) -> UserSchema:
    return await create_object(db=db, model=User, obj=user, response_model=UserSchema)


async def update_user(
    db: AsyncSession, user_id: int, user: UserUpdate
) -> Optional[UserSchema]:
    return await update_object(
        db=db,
        model=User,
        model_id=user_id,
        obj=user,
        response_model=UserSchema,
    )


async def delete_user(db: AsyncSession, user_id: int) -> Optional[int]:
    return await delete_object(db=db, model=User, model_id=user_id)
