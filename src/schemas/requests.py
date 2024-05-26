# --------------------------------------------------------------------------
# Request schemas를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field

from .responses import UserBase


# --------------------------------------------------------------------------
# User
# --------------------------------------------------------------------------
class UserCreate(UserBase):
    first_name: str
    last_name: str
    nickname: str
    password: str = Field(
        ..., title="User's password", description="유저 계정의 비밀번호 입니다."
    )


class UserUpdate(BaseModel):
    bio: str
    profile_img: str


class UserLogin(BaseModel):
    identifier: str
    password: str
