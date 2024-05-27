# --------------------------------------------------------------------------
# OpenAPI generator가 읽을 API 문서 내용을 정의하는 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from fastapi import FastAPI


def add_description_at_api_tags(app: FastAPI):
    tag_descriptions = {
        "user": "User API. 회원 로그인, 로그아웃, 정보 조회 및 수정 등을 수행합니다."
    }

    # OpenAPI 태그별 description 생성
    openapi_tags = [
        {"name": tag, "description": desc} for tag, desc in tag_descriptions.items()
    ]

    if app.openapi_tags:
        app.openapi_tags.extend(openapi_tags)
    else:
        app.openapi_tags = openapi_tags
