# --------------------------------------------------------------------------
# Order의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest_asyncio

from datetime import datetime, timedelta
from httpx import AsyncClient


class TestOrderAPI:
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

        self.listing_data = {
            "seller_id": self.user_id,
            "created_at": datetime.utcnow().isoformat(),
            "is_closed": False,
            "detail": "Test listing",
            "seller_info": "Test seller",
            "promotion_start": datetime.utcnow().isoformat(),
            "promotion_end": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "amount": 100,
        }
        response = await app_client.post(
            "kbuddy/api/v1/listing/", json=self.listing_data
        )
        self.listing_id = response.json()["id"]
        assert response.status_code == 200

        self.order_data = {
            "amount": 100,
            "is_refunded": False,
            "buyer_id": self.user_id,
            "listing_id": self.listing_id,
        }
        response = await app_client.post("kbuddy/api/v1/order/", json=self.order_data)
        self.order_id = response.json()["id"]
        assert response.status_code == 200

    async def test_create_order(self, app_client: AsyncClient):
        # given

        # when
        order_data = {
            "amount": 150,
            "is_refunded": False,
            "buyer_id": self.user_id,
            "listing_id": self.listing_id,
        }
        response = await app_client.post("kbuddy/api/v1/order/", json=order_data)

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == order_data["amount"]
        assert "id" in data

    async def test_get_all_orders(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get("kbuddy/api/v1/order/")

        # then
        assert response.status_code == 200
        assert len(response.json()) > 0

    async def test_get_order(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get(f"kbuddy/api/v1/order/{self.order_id}")

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == self.order_data["amount"]
        assert "id" in data

    async def test_update_order(self, app_client: AsyncClient):
        # given

        # when
        update_data = {
            "amount": 200,
            "is_refunded": True,
        }
        response = await app_client.put(
            f"kbuddy/api/v1/order/{self.order_id}",
            json=update_data,
        )

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == update_data["amount"]
        assert data["is_refunded"] == update_data["is_refunded"]

    async def test_delete_order(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.delete(f"kbuddy/api/v1/order/{self.order_id}")

        # then
        assert response.status_code == 204
