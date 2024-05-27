# --------------------------------------------------------------------------
# Request schemas를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from .responses import UserBase


# --------------------------------------------------------------------------
# User
# --------------------------------------------------------------------------
class UserCreate(UserBase):
    first_name: str = Field(
        ..., title="User's first name", description="유저의 실제 이름 입니다."
    )
    last_name: str = Field(
        ..., title="User's last name", description="유저의 실제 성 입니다."
    )
    nickname: str = Field(
        ..., title="User's nickname", description="유저의 닉네임 입니다."
    )
    email: EmailStr = Field(
        ..., title="User's Email", description="유저의 이메일 주소입니다."
    )
    password: str = Field(
        ..., title="User's password", description="유저 계정의 비밀번호 입니다."
    )


class UserUpdate(BaseModel):
    bio: str = Field(None, title="User's bio", description="유저의 한줄 소개 입니다.")
    profile_img: str = Field(
        None, title="User's profile image", description="유저의 프로필 이미지 입니다."
    )


class UserLogin(BaseModel):
    identifier: str = Field(
        ...,
        title="User's identifier",
        description="유저를 식별하는 identifier(UID 혹은 email) 입니다.",
    )
    password: str = Field(
        ..., title="User's password", description="유저 계정의 비밀번호 입니다."
    )
