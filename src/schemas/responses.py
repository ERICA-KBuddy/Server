# --------------------------------------------------------------------------
# Response schemas를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr, SecretStr, field_serializer, ConfigDict
from typing import Optional


# --------------------------------------------------------------------------
# User
# --------------------------------------------------------------------------
class UserBase(BaseModel):
    email: Optional[EmailStr] = Field(
        None, title="User's Email", description="유저의 이메일 주소입니다."
    )
    password: Optional[SecretStr] = Field(
        None, title="User's password", description="유저 계정의 비밀번호 입니다."
    )
    nickname: Optional[str] = Field(
        None, title="User's nickname", description="유저의 닉네임 입니다."
    )
    create_at: Optional[datetime] = Field(
        None,
        title="User's account created time",
        description="유저 계정의 생성 시간입니다.",
    )
    bio: str = Field(None, title="User's bio", description="유저의 한줄 소개 입니다.")
    point: Optional[int] = Field(
        None, title="User's point amount", description="유저의 포인트 입니다."
    )
    profile_img: Optional[str] = Field(
        None, title="User's profile image", description="유저의 프로필 이미지 입니다."
    )
    first_name: Optional[str] = Field(
        None, title="User's first name", description="유저의 실제 이름 입니다."
    )
    last_name: Optional[str] = Field(
        None, title="User's last name", description="유저의 실제 성 입니다."
    )

    @field_serializer("password", when_used="json")
    def dump_secret(self, v):
        return v.get_secret_value()


class UserSchema(UserBase):
    id: UUID = Field(
        ..., title="User's ID (pk)", description="유저의 고유 식별자입니다."
    )

    class Config:
        from_attributes = True
