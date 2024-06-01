# TODO: Itinerary testcase 추가 (request는 추가 완료, 검증 X)
# --------------------------------------------------------------------------
# Itinerary의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest_asyncio

from datetime import datetime, timedelta, date
from httpx import AsyncClient


class TestItineraryAPI:
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

        self.listing_data = {
            "seller_id": self.user_id,
            "created_at": datetime.utcnow().isoformat(),
            "is_closed": False,
            "detail": "Test listing",
            "seller_info": "Test seller",
            "promotion_start": datetime.utcnow().isoformat(),
            "promotion_end": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "amount": 10000,
        }
        response = await app_client.post(
            "kbuddy/api/v1/listing/", json=self.listing_data
        )
        self.listing_id = response.json()["id"]
        assert response.status_code == 200

        self.order_data = {
            "amount": 150,
            "is_refunded": False,
            "buyer_id": self.user_id,
            "listing_id": self.listing_id,
        }
        response = await app_client.post("kbuddy/api/v1/order/", json=self.order_data)
        self.order_id = response.json()["id"]
        assert response.status_code == 200

        self.itinerary_request_data = {
            "listing_id": self.listing_id,
            "order_id": self.order_id,
            "request_user_id": self.user_id,
            "first_name": "Test",
            "last_name": "User",
            "birthday": date(1990, 1, 1).isoformat(),
            "person_under": 2,
            "person_over": 2,
            "contact_method": "email",
            "contact": "test@example.com",
            "travel_start": date(2024, 1, 1).isoformat(),
            "travel_end": date(2024, 1, 10).isoformat(),
            "travel_purpose": "Vacation",
            "travel_pri": ["Activities", "Nature"],
            "transport_pri": ["Taxi", "Public"],
            "travel_restrict": "None",
            "travel_addi": "None",
        }
        response = await app_client.post(
            "kbuddy/api/v1/itinerary/request/", json=self.itinerary_request_data
        )
        self.itinerary_request_id = response.json()["id"]
        assert response.status_code == 200

    async def test_create_itinerary_request(self, app_client: AsyncClient):
        # given

        # when
        itinerary_request_data = {
            "listing_id": self.listing_id,
            "order_id": self.order_id,
            "request_user_id": self.user_id,
            "first_name": "New",
            "last_name": "User",
            "birthday": date(1991, 1, 1).isoformat(),
            "person_under": 1,
            "person_over": 1,
            "contact_method": "phone",
            "contact": "new@example.com",
            "travel_start": date(2024, 2, 1).isoformat(),
            "travel_end": date(2024, 2, 10).isoformat(),
            "travel_purpose": "Business",
            "travel_pri": ["Cuisine"],
            "transport_pri": ["Car"],
            "travel_restrict": "None",
            "travel_addi": "None",
        }
        response = await app_client.post(
            "kbuddy/api/v1/itinerary/request/", json=itinerary_request_data
        )

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == itinerary_request_data["first_name"]
        assert "id" in data

    async def test_get_all_itinerary_requests(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get("kbuddy/api/v1/itinerary/request/")

        # then
        assert response.status_code == 200
        assert len(response.json()) > 0

    async def test_get_itinerary_request(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get(
            f"kbuddy/api/v1/itinerary/request/{self.itinerary_request_id}"
        )

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == self.itinerary_request_data["first_name"]
        assert "id" in data

    async def test_delete_itinerary_request(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.post(
            f"kbuddy/api/v1/itinerary/request/{self.itinerary_request_id}/delete"
        )

        # then
        assert response.status_code == 204
