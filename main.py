# --------------------------------------------------------------------------
# FastAPI application과 runner을 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from __future__ import annotations

import uvicorn

from src import create_app, init_logger
from src.core.settings import settings

init_logger(settings)

app = create_app(settings)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_DOMAIN,
        port=settings.SERVER_PORT,
        reload=True,
    )
