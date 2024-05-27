# --------------------------------------------------------------------------
# User의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import json
import pytest_asyncio

from httpx import AsyncClient


class TestUserAPI:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, app_client: AsyncClient):
        self.user_data = {
            "email": "bnbong@hanyang.ac.kr",
            "password": "password123",
            "nickname": "bnbong",
            "bio": "Hello world!",
            "first_name": "JunHyeok",
            "last_name": "Lee",
        }
        response = await app_client.post(
            "kbuddy/api/v1/user/signup", json=self.user_data
        )
        self.user_id = response.json()["id"]
        assert response.status_code == 200

    async def test_create_user(self, app_client: AsyncClient):
        # given

        # when
        user_data = {
            "email": "testuser@example.com",
            "password": "password123",
            "nickname": "testuser",
            "bio": "This is a test user",
            "first_name": "Test",
            "last_name": "User",
        }
        response = await app_client.post("kbuddy/api/v1/user/signup", json=user_data)

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
        assert "id" in data

    async def test_user_login(self, app_client: AsyncClient):
        # given

        # then
        login_data = {"identifier": "bnbong@hanyang.ac.kr", "password": "password123"}
        response = await app_client.post("kbuddy/api/v1/user/login", json=login_data)

        # then
        assert response.status_code == 200
        data = response.json()["user"]
        data = json.loads(data)
        assert data["email"] == self.user_data["email"]
        assert "id" in data

    async def test_user_logout(self, app_client: AsyncClient):
        # given
        login_data = {"identifier": "bnbong@hanyang.ac.kr", "password": "password123"}
        response = await app_client.post("kbuddy/api/v1/user/login", json=login_data)
        assert response.status_code == 200  # 유저가 존재하고 로그인이 되어 있다는 상황
        cookies = response.cookies

        # when
        response = await app_client.post("kbuddy/api/v1/user/logout", cookies=cookies)

        # then
        assert response.status_code == 204
        assert response.json() == "성공적으로 로그아웃 하였습니다."

    async def test_get_all_users(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get("kbuddy/api/v1/user/list")

        # then
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["email"] == "bnbong@hanyang.ac.kr"

    async def test_get_a_user(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get(f"kbuddy/api/v1/user/{self.user_id}")

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == self.user_data["email"]
        assert "id" in data

    async def test_edit_user_info(self, app_client: AsyncClient):
        # given
        login_data = {"identifier": "bnbong@hanyang.ac.kr", "password": "password123"}
        response = await app_client.post("kbuddy/api/v1/user/login", json=login_data)
        assert response.status_code == 200  # 유저가 존재하고 로그인이 되어 있다는 상황
        cookies = response.cookies

        # when
        update_data = {
            "bio": "Updated bio",
            "profile_img": "http://example.com/updated.jpg",
        }
        response = await app_client.put(
            f"kbuddy/api/v1/user/{self.user_id}",
            json=update_data,
            cookies=cookies,
        )

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["bio"] == update_data["bio"]
        assert data["profile_img"] == update_data["profile_img"]

    async def test_delete_user(self, app_client: AsyncClient):
        # given
        login_data = {"identifier": "bnbong@hanyang.ac.kr", "password": "password123"}
        response = await app_client.post("kbuddy/api/v1/user/login", json=login_data)
        assert response.status_code == 200  # 유저가 존재하고 로그인이 되어 있다는 상황
        cookies = response.cookies

        # when
        response = await app_client.post(
            f"kbuddy/api/v1/user/{self.user_id}/withdraw",
            cookies=cookies,
        )

        # then
        assert response.status_code == 204
