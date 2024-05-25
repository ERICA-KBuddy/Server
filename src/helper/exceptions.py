# --------------------------------------------------------------------------
# Backend Application의 Exception class를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from enum import Enum

from pydantic import BaseModel, Field


class ErrorCode(Enum):
    NOT_FOUND = ("NOT_FOUND", "KB-001", 404)
    UNKNOWN_ERROR = ("UNKNOWN_ERROR", "KB-002", 500)
    FORBIDDEN = ("FORBIDDEN", "KB-003", 403)
    BAD_REQUEST = ("BAD_REQUEST", "KB-004", 400)


class ExceptionSchema(BaseModel):
    timestamp: str = Field(
        ...,
        description="에러가 발생한 시간입니다.",
    )
    status: int = Field(..., description="에러의 HTTP status code 입니다.")
    error: str = Field(
        ...,
        description="에러의 이름입니다.",
    )
    message: str = Field(
        ...,
        description="에러의 메시지 내용입니다.",
    )
    errorCode: str = Field(
        ...,
        description="에러의 코드입니다.",
    )
    path: str = Field(
        ...,
        description="에러가 발생한 경로입니다.",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "default": {
                    "timestamp": "2021-10-17T16:55:00.000000Z",
                    "status": 500,
                    "error": "INTERNAL_SERVER_ERROR",
                    "message": "서버 로직에 알 수 없는 오류가 발생했습니다.",
                    "errorCode": "KB-000",
                    "path": "/v1/<some/endpoint>",
                }
            }
        }


class InternalException(Exception):
    def __init__(self, message: str, error_code: ErrorCode):
        self.message = message
        self.error_code = error_code
