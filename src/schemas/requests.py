# --------------------------------------------------------------------------
# Request schemas를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from enum import Enum
from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

from .responses import (
    UserBase,
    AreaBase,
    AreaImageBase,
    PointDetailBase,
    PointEventBase,
    ListingBase,
    OrderBase,
    ItineraryBase,
    ItineraryRequestBase,
)


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


# --------------------------------------------------------------------------
# Area
# --------------------------------------------------------------------------
class AreaCreate(AreaBase):
    pass


class AreaUpdate(AreaBase):
    pass


class AreaImageCreate(AreaImageBase):
    pass


class AreaImageUpdate(AreaImageBase):
    pass


# --------------------------------------------------------------------------
# Hashtag
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Review
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Listing
# --------------------------------------------------------------------------
class ListingCreate(ListingBase):
    pass


class ListingUpdate(BaseModel):
    is_closed: Optional[bool]
    detail: Optional[str]
    seller_info: Optional[str]
    promotion_start: Optional[datetime]
    promotion_end: Optional[datetime]
    amount: Optional[int]


# --------------------------------------------------------------------------
# Order
# --------------------------------------------------------------------------
class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    amount: Optional[int]
    is_refunded: Optional[bool]


# --------------------------------------------------------------------------
# Itinerary
# --------------------------------------------------------------------------
class ItineraryRequestCreate(ItineraryRequestBase):
    pass


class ItineraryRequestUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    birthday: Optional[date]
    person_under: Optional[int]
    person_over: Optional[int]
    contact_method: Optional[str]
    contact: Optional[str]
    travel_start: Optional[date]
    travel_end: Optional[date]
    travel_purpose: Optional[str]
    travel_pri: Optional[str]
    transport_pri: Optional[str]
    travel_restrict: Optional[str]
    travel_addi: Optional[str]


class ItineraryCreate(ItineraryBase):
    pass


# --------------------------------------------------------------------------
# Point
# --------------------------------------------------------------------------
class PointEventCreate(PointEventBase):
    pass


class PointEventUpdate(PointEventBase):
    pass


class PointDetailCreate(PointDetailBase):
    pass


class PointDetailUpdate(PointDetailBase):
    pass
