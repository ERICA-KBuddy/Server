# --------------------------------------------------------------------------
# Member model을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import uuid

from sqlalchemy import (
    Integer,
    String,
    Column,
    ForeignKey,
    Boolean,
    Text,
    Date,
    TIMESTAMP,
    UUID as SQLUUID,
)
from sqlalchemy.orm import relationship

from src.db._base import ModelBase


class User(ModelBase):
    __tablename__ = "Users"
    id = Column(SQLUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(256), nullable=True)
    password = Column(String(256), nullable=True)
    nickname = Column(String(30), nullable=True)
    create_at = Column(TIMESTAMP, nullable=True)
    bio = Column(String(50), nullable=False)
    point = Column(Integer, nullable=True)
    profile_img = Column(String(2048), nullable=True)

    reviews = relationship("UserReview", back_populates="reviewer")
    point_events = relationship("PointEvent", back_populates="user")


class Hashtag(ModelBase):
    __tablename__ = "Hashtag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id2 = Column(SQLUUID(as_uuid=True), nullable=False)
    tag = Column(String(100), nullable=False)


class Listing(ModelBase):
    __tablename__ = "Listing"
    id = Column(SQLUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id = Column(SQLUUID(as_uuid=True), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    is_closed = Column(Boolean, nullable=False)
    detail = Column(Text, nullable=False)
    seller_info = Column(Text, nullable=False)
    promotion_start = Column(TIMESTAMP, nullable=False)
    promotion_end = Column(TIMESTAMP, nullable=False)
    amount = Column(Integer, nullable=False)


class ItineraryRequest(ModelBase):
    __tablename__ = "Itinerary_Request"
    id = Column(SQLUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id = Column(SQLUUID(as_uuid=True), ForeignKey("Listing.id"), nullable=False)
    order_id = Column(SQLUUID(as_uuid=True), nullable=False)
    request_user_id = Column(SQLUUID(as_uuid=True), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(25), nullable=False)
    birthday = Column(Date, nullable=False)
    person_under = Column(Integer, nullable=True)
    person_over = Column(Integer, nullable=True)
    contact_method = Column(String, nullable=False)
    contact = Column(String(100), nullable=False)
    travel_start = Column(Date, nullable=False)
    travel_end = Column(Date, nullable=False)
    travel_purpose = Column(Text, nullable=False)
    travel_pri = Column(Text, nullable=False)
    transport_pri = Column(Text, nullable=False)
    travel_restrict = Column(Text, nullable=True)
    travel_addi = Column(Text, nullable=True)

    itinerary = relationship("Itinerary", back_populates="request")
    place_containers = relationship("PlaceContainer", back_populates="request")
    transport_containers = relationship("TransportContainer", back_populates="request")


class Order(ModelBase):
    __tablename__ = "Orders"
    id = Column(SQLUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(Integer, nullable=False)
    is_refunded = Column(Boolean, nullable=False)
    buyer_id = Column(SQLUUID(as_uuid=True), nullable=False)
    listing_id = Column(SQLUUID(as_uuid=True), ForeignKey("Listing.id"), nullable=False)


class Itinerary(ModelBase):
    __tablename__ = "Itinerary"
    id = Column(SQLUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(
        SQLUUID(as_uuid=True), ForeignKey("Itinerary_Request.id"), nullable=False
    )

    request = relationship("ItineraryRequest", back_populates="itinerary")
    place_containers = relationship("PlaceContainer", back_populates="itinerary")
    transport_containers = relationship(
        "TransportContainer", back_populates="itinerary"
    )


class PlaceContainer(ModelBase):
    __tablename__ = "Place_Container"
    id = Column(Integer, primary_key=True, autoincrement=True)
    itinerary_id = Column(
        SQLUUID(as_uuid=True), ForeignKey("Itinerary.id"), nullable=False
    )
    request_id = Column(
        SQLUUID(as_uuid=True), ForeignKey("Itinerary_Request.id"), nullable=False
    )
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    container_date = Column(Date, nullable=False)

    itinerary = relationship("Itinerary", back_populates="place_containers")
    request = relationship("ItineraryRequest", back_populates="place_containers")


class TransportContainer(ModelBase):
    __tablename__ = "Transport_Container"
    id = Column(Integer, primary_key=True, autoincrement=True)
    itinerary_id = Column(
        SQLUUID(as_uuid=True), ForeignKey("Itinerary.id"), nullable=False
    )
    request_id = Column(
        SQLUUID(as_uuid=True), ForeignKey("Itinerary_Request.id"), nullable=False
    )
    type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)
    container_date = Column(Date, nullable=False)

    itinerary = relationship("Itinerary", back_populates="transport_containers")
    request = relationship("ItineraryRequest", back_populates="transport_containers")


class UserReview(ModelBase):
    __tablename__ = "User_Review"
    id = Column(Integer, primary_key=True, autoincrement=True)
    reviewer_id = Column(SQLUUID(as_uuid=True), ForeignKey("Users.id"), nullable=False)
    detail = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    reviewer = relationship("User", back_populates="reviews")


class Area(ModelBase):
    __tablename__ = "Area"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(512), nullable=False)
    website = Column(Text, nullable=True)
    contact_num = Column(String(100), nullable=True)
    open_time = Column(Text, nullable=True)


class AreaReview(ModelBase):
    __tablename__ = "Area_Review"
    id = Column(Integer, primary_key=True, autoincrement=True)
    area_id = Column(Integer, ForeignKey("Area.id"), nullable=False)
    reviewer_id = Column(SQLUUID(as_uuid=True), nullable=False)
    detail = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)


class AreaImage(ModelBase):
    __tablename__ = "Area_Image"
    id = Column(Integer, primary_key=True, autoincrement=True)
    area_id = Column(Integer, ForeignKey("Area.id"), nullable=False)
    area_img = Column(String(2048), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)


class PointEvent(ModelBase):
    __tablename__ = "Point_Event"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(SQLUUID(as_uuid=True), ForeignKey("Users.id"), nullable=False)
    event_type = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    detail = Column(String(100), nullable=False)
    event_date = Column(TIMESTAMP, nullable=False)
    exp_date = Column(TIMESTAMP, nullable=True)

    user = relationship("User", back_populates="point_events")


class PointDetail(ModelBase):
    __tablename__ = "Point_Detail"
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("Point_Event.id"), nullable=False)
    related_event_id = Column(Integer, ForeignKey("Point_Event.id"), nullable=False)
    point_date = Column(TIMESTAMP, nullable=False)
    point = Column(Integer, nullable=False)
