# --------------------------------------------------------------------------
# Backend Application의 패키지 정보를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
from setuptools import setup, find_packages

install_requires = [
    # Main Application Dependencies
    "fastapi==0.104.0",
    "uvicorn==0.23.2",
    "uvloop==0.18.0",
    "websockets==11.0.3",
    "httpx==0.25.0",
    # ORM Dependencies
    "pydantic==2.4.2",
    "pydantic_core==2.10.1",
    "pydantic-settings==2.0.3",
    "SQLAlchemy==2.0.22",
    "PyMySQL==1.1.0",
    "alembic==1.12.0",
    "aiomysql==0.2.0",
    # Utility Dependencies
    "python-dotenv==1.0.0",
    "starlette==0.27.0",
    "greenlet==3.0.0",
    "typing_extensions==4.8.0",
    "watchfiles==0.21.0",
    "pytest==7.4.2",
    "pytest-asyncio==0.21.1",
]

# IDE will watch this setup config through your project src, and help you to set up your environment
setup(
    name="fastapi-simplebackend",
    description="Simple API server for test",
    author="bnbong",
    author_email="bbbong9@gmail.com",
    packages=find_packages(where="app"),
    use_scm_version=True,
    requires=["python (>=3.10)"],
    install_requires=install_requires,
)
