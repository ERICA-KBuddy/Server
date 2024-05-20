# --------------------------------------------------------------------------
# Backned Application의 Exception class를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from enum import Enum


class ErrorCode(Enum):
    NOT_FOUND = ("NOT_FOUND", "FS-001", 404)
    UNKNOWN_ERROR = ("UNKNOWN_ERROR", "FS-002", 500)
    FORBIDDEN = ("FORBIDDEN", "FS-003", 403)


class InternalException(Exception):
    def __init__(self, message: str, error_code: ErrorCode):
        self.message = message
        self.error_code = error_code
