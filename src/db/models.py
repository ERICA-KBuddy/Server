# --------------------------------------------------------------------------
# Member model을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.db._base import ModelBase


class Item(ModelBase):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(length=255), index=True)
    price = Column(Integer, index=True)
    owner_id = Column(Integer, ForeignKey("member.id"))

    owner = relationship("Member", back_populates="items")
