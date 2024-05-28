# TODO: 본인이 작성하거나 구매한 여행기만 확인할 수 있도록 수정
# --------------------------------------------------------------------------
# Itinerary model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import itinerary as crud
from src.db import database
from src.helper.exceptions import InternalException, ErrorCode


log = getLogger(__name__)
itinerary_router = APIRouter(prefix="/itinerary")
