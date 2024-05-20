# TODO: Failure test case 추가
# --------------------------------------------------------------------------
# Item의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest_asyncio

from httpx import AsyncClient


async def _create_item(app_client: AsyncClient, name: str, price: int, owner_id: int):
    """Helper function to create an item and return the id"""
    response = await app_client.post(
        "api/v1/item/", json={"name": name, "price": price, "owner_id": owner_id}
    )
    return response.json()


class TestItemAPI:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, app_client: AsyncClient):
        self.test_item = await _create_item(
            app_client, "Apple", 1000, self.test_user["id"]
        )

    async def test_create_item(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.post(
            "api/v1/item/",
            json={
                "name": "Test Item",
                "price": 10000,
                "owner_id": self.test_user["id"],
            },
        )

        # then
        data = response.json()
        assert response.status_code == 200
        assert data["name"] == "Test Item"
        assert data["price"] == 10000

    async def test_read_item(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get(f"api/v1/item/{self.test_item['id']}")

        # then
        data = response.json()
        assert response.status_code == 200
        assert data["name"] == "Apple"
        assert data["price"] == 1000

    async def test_read_items(self, app_client: AsyncClient):
        # given
        for i in range(10):
            await _create_item(app_client, f"Test Item {i}", 1000, self.test_user["id"])

        # when
        response = await app_client.get(f"api/v1/item/")

        # then
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 11

    async def test_update_item(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.put(
            f"api/v1/item/{self.test_item['id']}",
            json={"name": "Apple", "price": 2000},
        )

        # then
        data = response.json()
        assert response.status_code == 200
        assert data["name"] == "Apple"
        assert data["price"] == 2000

    async def test_delete_item(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.delete(f"api/v1/item/{self.test_item['id']}")

        # then
        data = response.json()
        assert response.status_code == 200
        assert data == self.test_item["id"]
