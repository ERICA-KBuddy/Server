# --------------------------------------------------------------------------
# 유저 인증 로직을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger

from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.user import get_user_by_email
from src.helper.exceptions import InternalException, ErrorCode
from src.db import database
from src.utils.authentication import decode_user_data_from_token

log = getLogger(__name__)


def auth(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise InternalException("인증 정보가 없습니다.", ErrorCode.BAD_REQUEST)


async def get_auth_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    return await decode_user_data_from_token(token=token)


async def get_current_user_info(
    request: Request, db: AsyncSession = Depends(database.get_db)
):
    token_data, user_email = await get_auth_from_cookie(request=request)
    user = await get_user_by_email(db=db, user_email=user_email)
    if user is None:
        raise InternalException("유저를 찾을 수 없습니다.", ErrorCode.NOT_FOUND)
    return user


async def check_user(
    request: Request,
) -> str:
    _, user_pk = await get_auth_from_cookie(request)
    if not user_pk:
        raise InternalException("사용자 정보가 없습니다.", ErrorCode.BAD_REQUEST)
    return user_pk


async def check_user_is_self(
    request: Request,
    target_pk: str,
    db: AsyncSession = Depends(database.get_db),
):
    request_user = await get_current_user_info(request=request, db=db)
    if not request_user:
        raise InternalException("유저를 찾을 수 없습니다.", ErrorCode.NOT_FOUND)
    if str(request_user.id) != target_pk:
        raise InternalException("해당 작업은 본인만 가능합니다.", ErrorCode.FORBIDDEN)

    return request_user
