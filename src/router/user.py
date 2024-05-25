# --------------------------------------------------------------------------
# User model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import user as crud
from src.db import database
from src.helper.exceptions import InternalException, ErrorCode
from src.schemas.requests import UserCreate, UserUpdate
from src.schemas.responses import UserSchema
from ._check import auth, check_user, check_user_is_self


log = getLogger(__name__)
user_router = APIRouter(prefix="/user")


@user_router.get(
    "/list",
    response_model=List[UserSchema],
    summary="회원 전체를 불러오기",
    description="모든 회원에 대한 정보를 조회합니다.",
)
async def get_all_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)
):
    log.info(f"Reading students info with skip: {skip} and limit: {limit}")
    return await crud.get_all_users(db, skip=skip, limit=limit)


# get a user
@user_router.get(
    "/{user_id}",
    response_model=UserSchema,
    summary="단일 회원 조회",
    description="회원 정보를 조회합니다.",
)
async def read_user(user_id: int, db: AsyncSession = Depends(database.get_db)):
    db_user = await crud.get_user(db, user_id)
    if db_user is None:
        raise InternalException("해당 유저를 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND)
    return db_user


# create a user
@user_router.post(
    "/",
    response_model=UserSchema,
    summary="단일 회원 추가",
    description="회원 정보를 추가합니다.",
)
async def create_user(user: UserCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_user(db, user)


# edit a user's info
@user_router.put(
    "/{user_id}",
    response_model=UserSchema,
    summary="단일 회원 정보 수정",
    description="회원 정보를 수정합니다.",
    dependencies=[Depends(auth)],
)
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: AsyncSession = Depends(database.get_db),
    request_user=Depends(check_user),
):
    user_pk = request_user
    await check_user_is_self(db=db, user_pk=int(user_pk), target_pk=user_id)

    db_user = await crud.get_user(db, user_id)
    if db_user is None:
        raise InternalException("해당 유저를 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND)
    return await crud.update_user(db, user_id, user)


# delete a user
@user_router.delete(
    "/{user_id}",
    status_code=204,
    summary="단일 회원 삭제",
    description="회원을 삭제합니다.",
    dependencies=[Depends(auth)],
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(database.get_db),
    request_user=Depends(check_user),
):
    user_pk = request_user
    await check_user_is_self(db=db, user_pk=int(user_pk), target_pk=user_id)

    db_user = await crud.get_user(db, user_id)
    if db_user is None:
        raise InternalException("해당 유저를 찾을 수 없습니다.", error_code=ErrorCode.NOT_FOUND)
    return await crud.delete_user(db, user_id)

# user login

# user logout
