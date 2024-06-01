# --------------------------------------------------------------------------
# Response schemas를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from datetime import datetime, date
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, Field, EmailStr, SecretStr, field_serializer
from typing import Optional, List


# --------------------------------------------------------------------------
# Area
# --------------------------------------------------------------------------
class AreaBase(BaseModel):
    name: str
    address: str
    website: Optional[str] = None
    contact_num: Optional[str] = None
    open_time: Optional[str] = None


class AreaImageBase(BaseModel):
    area_img: str
    created_at: datetime


class AreaImageSchema(AreaImageBase):
    id: int
    area_id: int

    class Config:
        from_attributes = True


class AreaSchema(AreaBase):
    id: int
    images: List[AreaImageSchema] = []

    class Config:
        from_attributes = True


# --------------------------------------------------------------------------
# Hashtag
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Review
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Listing
# --------------------------------------------------------------------------
class ListingBase(BaseModel):
    seller_id: UUID
    created_at: datetime
    is_closed: bool
    detail: str
    seller_info: str
    promotion_start: datetime
    promotion_end: datetime
    amount: int


class ListingSchema(ListingBase):
    id: UUID

    class Config:
        from_attributes = True


# --------------------------------------------------------------------------
# Order
# --------------------------------------------------------------------------
class OrderBase(BaseModel):
    amount: int
    is_refunded: bool
    buyer_id: UUID
    listing_id: UUID


class OrderSchema(OrderBase):
    id: UUID

    class Config:
        from_attributes = True


# --------------------------------------------------------------------------
# Itinerary
# --------------------------------------------------------------------------
class TransportPriEnum(str, Enum):
    TAXI = "Taxi"
    CAR = "Car"
    PUBLIC = "Public"


class TravelPriEnum(str, Enum):
    ACTIVITIES = "Activities"
    BUDGET = "Budget"
    CULTURE = "Culture (Local traditions)"
    CUISINE = "Cuisine"
    HISTORY = "History"
    LOCAL_EVENTS = "Local events"
    NATURE = "Nature"
    PHOTOGRAPHY = "Photography"
    RELAXATION = "Relaxation"
    SHOPPING = "Shopping"


class ItineraryRequestBase(BaseModel):
    listing_id: UUID
    order_id: UUID
    request_user_id: UUID
    first_name: str
    last_name: str
    birthday: date
    person_under: Optional[int]
    person_over: Optional[int]
    contact_method: str
    contact: str
    travel_start: date
    travel_end: date
    travel_purpose: str
    travel_pri: List[TravelPriEnum]
    transport_pri: List[TransportPriEnum]
    travel_restrict: Optional[str]
    travel_addi: Optional[str]


class ItineraryRequestSchema(ItineraryRequestBase):
    id: UUID

    class Config:
        from_attributes = True


class ItineraryBase(BaseModel):
    request_id: UUID


class PlaceContainerSchema(BaseModel):
    id: int
    itinerary_id: UUID
    request_id: UUID
    name: str
    description: str
    container_date: date

    class Config:
        from_attributes = True


class TransportContainerSchema(BaseModel):
    id: int
    itinerary_id: UUID
    request_id: UUID
    type: str
    description: str
    duration: int
    container_date: date

    class Config:
        from_attributes = True


class ItinerarySchema(ItineraryBase):
    id: UUID
    place_containers: List[PlaceContainerSchema]
    transport_containers: List[TransportContainerSchema]

    class Config:
        from_attributes = True


# --------------------------------------------------------------------------
# Point
# --------------------------------------------------------------------------
class PointEventBase(BaseModel):
    user_id: UUID
    event_type: str
    amount: int
    detail: str
    event_date: datetime
    exp_date: Optional[datetime]


class PointEventSchema(PointEventBase):
    id: int

    class Config:
        from_attributes = True


class PointDetailBase(BaseModel):
    event_id: int
    related_event_id: int
    point_date: datetime
    point: int


class PointDetailSchema(PointDetailBase):
    id: int

    class Config:
        from_attributes = True


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

    # itinerary_requests: Optional[List] = List[ItineraryRequestSchema]
    # listings: Optional[List] = List[ListingSchema]

    @field_serializer("password", when_used="json")
    def dump_secret(self, v):
        return v.get_secret_value()


class UserSchema(UserBase):
    id: UUID = Field(
        ..., title="User's ID (pk)", description="유저의 고유 식별자입니다."
    )

    class Config:
        from_attributes = True
