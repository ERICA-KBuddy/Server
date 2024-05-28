# --------------------------------------------------------------------------
# Listing의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import random
import pytest_asyncio

from datetime import datetime, timedelta
from httpx import AsyncClient


class TestListingAPI:
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
        response = await app_client.post("kbuddy/api/v1/user/signup", json=self.user_data)
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
        response = await app_client.post("kbuddy/api/v1/listing/", json=self.listing_data)
        self.listing_id = response.json()["id"]
        assert response.status_code == 200

    async def test_create_listing(self, app_client: AsyncClient):
        # given

        # when
        listing_data = {
            "seller_id": self.user_id,
            "created_at": datetime.utcnow().isoformat(),
            "is_closed": False,
            "detail": "New listing",
            "seller_info": "New seller",
            "promotion_start": datetime.utcnow().isoformat(),
            "promotion_end": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "amount": 200,
        }
        response = await app_client.post("kbuddy/api/v1/listing/", json=listing_data)

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["detail"] == listing_data["detail"]
        assert "id" in data

    async def test_get_all_listings(self, app_client: AsyncClient):
        # given
        for i in range(5):
            random_days = random.randint(1, 365)
            listing_data = {
                "seller_id": self.user_id,
                "created_at": datetime.utcnow().isoformat(),
                "is_closed": False,
                "detail": f"New listing {i}",
                "seller_info": "This is seller information",
                "promotion_start": datetime.utcnow().isoformat(),
                "promotion_end": (datetime.utcnow() + timedelta(days=random_days)).isoformat(),
                "amount": 200,
            }
            await app_client.post("kbuddy/api/v1/listing/", json=listing_data)

        # when
        response = await app_client.get("kbuddy/api/v1/listing/")

        # then
        assert response.status_code == 200
        data = response.json()
        assert len(response.json()) > 1
        assert data[1]["detail"] == "New listing 0"

    async def test_get_listing(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get(f"kbuddy/api/v1/listing/{self.listing_id}")

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["detail"] == self.listing_data["detail"]
        assert "id" in data

    async def test_update_listing(self, app_client: AsyncClient):
        # given

        # when
        update_data = {
            "is_closed": True,
            "detail": "Updated listing",
            "seller_info": "Updated seller",
            "promotion_start": datetime.utcnow().isoformat(),
            "promotion_end": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "amount": 300,
        }
        response = await app_client.put(
            f"kbuddy/api/v1/listing/{self.listing_id}",
            json=update_data,
        )

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["amount"] == update_data["amount"]
        assert data["detail"] == update_data["detail"]

    async def test_delete_listing(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.delete(f"kbuddy/api/v1/listing/{self.listing_id}")

        # then
        assert response.status_code == 204
