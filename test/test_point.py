# --------------------------------------------------------------------------
# Point의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest_asyncio

from datetime import datetime, timedelta
from httpx import AsyncClient


class TestPointAPI:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, app_client: AsyncClient):
        self.user_data = {
            "email": "testuser@example.com",
            "password": "password123",
            "nickname": "testuser",
            "bio": "Test bio",
            "first_name": "Test",
            "last_name": "User",
        }
        response = await app_client.post(
            "kbuddy/api/v1/user/signup", json=self.user_data
        )
        self.user_id = response.json()["id"]
        assert response.status_code == 200

        self.login_data = {
            "identifier": "testuser@example.com",
            "password": "password123",
        }
        await app_client.post("kbuddy/api/v1/user/login", json=self.login_data)

        self.event_data = {
            "user_id": self.user_id,
            "event_type": "earn",
            "amount": 100,
            "detail": "Test earning event",
            "event_date": datetime.utcnow().isoformat(),
            "exp_date": (datetime.utcnow() + timedelta(days=365)).isoformat(),
        }
        response = await app_client.post(
            "kbuddy/api/v1/point/events", json=self.event_data
        )
        self.event_id = response.json()["id"]
        assert response.status_code == 200

    async def test_create_point_event(self, app_client: AsyncClient):
        # given

        # when
        event_data = {
            "user_id": self.user_id,
            "event_type": "earn",
            "amount": 50,
            "detail": "New earning event",
            "event_date": datetime.utcnow().isoformat(),
            "exp_date": (datetime.utcnow() + timedelta(days=365)).isoformat(),
        }
        response = await app_client.post("kbuddy/api/v1/point/events", json=event_data)

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == event_data["amount"]
        assert "id" in data

    async def test_get_all_point_events(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get("kbuddy/api/v1/point/events")

        # then
        assert response.status_code == 200
        assert len(response.json()) > 0

    async def test_get_point_event(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get(f"kbuddy/api/v1/point/events/{self.event_id}")

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["detail"] == self.event_data["detail"]
        assert "id" in data

    async def test_update_point_event(self, app_client: AsyncClient):
        # given

        # when
        update_data = {
            "user_id": self.user_id,
            "event_type": "earn",
            "amount": 200,
            "detail": "Updated earning event",
            "event_date": datetime.utcnow().isoformat(),
            "exp_date": (datetime.utcnow() + timedelta(days=365)).isoformat(),
        }
        response = await app_client.put(
            f"kbuddy/api/v1/point/events/{self.event_id}",
            json=update_data,
        )

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == update_data["amount"]
        assert data["detail"] == update_data["detail"]

    async def test_delete_point_event(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.delete(
            f"kbuddy/api/v1/point/events/{self.event_id}"
        )

        # then
        assert response.status_code == 204

    async def test_create_point_detail(self, app_client: AsyncClient):
        # given
        detail_data = {
            "event_id": self.event_id,
            "related_event_id": self.event_id,
            "point_date": datetime.utcnow().isoformat(),
            "point": 50,
        }

        # when
        response = await app_client.post(
            "kbuddy/api/v1/point/details", json=detail_data
        )

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["point"] == detail_data["point"]
        assert "id" in data

    async def test_get_all_point_details(self, app_client: AsyncClient):
        # given
        detail_data = {
            "event_id": self.event_id,
            "related_event_id": self.event_id,
            "point_date": datetime.utcnow().isoformat(),
            "point": 50,
        }

        # when
        for i in range(5):
            await app_client.post("kbuddy/api/v1/point/details", json=detail_data)

        # when
        response = await app_client.get("kbuddy/api/v1/point/details")

        # then
        assert response.status_code == 200
        data = response.json()
        assert len(response.json()) > 0
        assert data[0]["point"] == 50

    async def test_get_point_detail(self, app_client: AsyncClient):
        # given
        detail_data = {
            "event_id": self.event_id,
            "related_event_id": self.event_id,
            "point_date": datetime.utcnow().isoformat(),
            "point": 50,
        }
        response = await app_client.post(
            "kbuddy/api/v1/point/details", json=detail_data
        )
        detail_id = response.json()["id"]

        # when
        response = await app_client.get(f"kbuddy/api/v1/point/details/{detail_id}")

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["point"] == detail_data["point"]
        assert "id" in data

    async def test_update_point_detail(self, app_client: AsyncClient):
        # given
        detail_data = {
            "event_id": self.event_id,
            "related_event_id": self.event_id,
            "point_date": datetime.utcnow().isoformat(),
            "point": 50,
        }
        response = await app_client.post(
            "kbuddy/api/v1/point/details", json=detail_data
        )
        detail_id = response.json()["id"]

        # when
        update_data = {
            "event_id": self.event_id,
            "related_event_id": self.event_id,
            "point_date": datetime.utcnow().isoformat(),
            "point": 100,
        }
        response = await app_client.put(
            f"kbuddy/api/v1/point/details/{detail_id}",
            json=update_data,
        )

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["point"] == update_data["point"]

    async def test_delete_point_detail(self, app_client: AsyncClient):
        # given
        detail_data = {
            "event_id": self.event_id,
            "related_event_id": self.event_id,
            "point_date": datetime.utcnow().isoformat(),
            "point": 50,
        }
        response = await app_client.post(
            "kbuddy/api/v1/point/details", json=detail_data
        )
        detail_id = response.json()["id"]

        # when
        response = await app_client.delete(f"kbuddy/api/v1/point/details/{detail_id}")

        # then
        assert response.status_code == 204

    async def test_get_user_point_balance(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get(
            f"kbuddy/api/v1/point/user/{self.user_id}/balance"
        )

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == self.user_id
        assert "balance" in data
