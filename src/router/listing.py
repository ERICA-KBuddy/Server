# --------------------------------------------------------------------------
# Listing model의 API router을 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from logging import getLogger
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import listing as crud
from src.db import database
from src.helper.exceptions import InternalException, ErrorCode


log = getLogger(__name__)
listing_router = APIRouter(prefix="/listing")
