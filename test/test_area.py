# --------------------------------------------------------------------------
# Area의 testcase를 정의한 모듈입니다.
#
# @author bnbong bbbong9@gmail.com
# --------------------------------------------------------------------------
import pytest_asyncio

from httpx import AsyncClient


class TestAreaAPI:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, app_client: AsyncClient):
        self.area_data = {
            "name": "Test Area",
            "address": "123 Test St",
            "website": "http://test.com",
            "contact_num": "123-456-7890",
            "open_time": "9:00 AM - 5:00 PM",
        }
        response = await app_client.post("kbuddy/api/v1/area/add", json=self.area_data)
        self.area_id = response.json()["id"]
        assert response.status_code == 200

    async def test_create_area(self, app_client: AsyncClient):
        # given

        # when
        area_data = {
            "name": "New Area",
            "address": "456 New St",
            "website": "http://new.com",
            "contact_num": "987-654-3210",
            "open_time": "10:00 AM - 6:00 PM",
        }
        response = await app_client.post("kbuddy/api/v1/area/add", json=area_data)

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == area_data["name"]
        assert "id" in data

    async def test_get_all_areas(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get("kbuddy/api/v1/area/list")

        # then
        assert response.status_code == 200
        assert len(response.json()) > 0

    async def test_get_a_area(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.get(f"kbuddy/api/v1/area/{self.area_id}")

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == self.area_data["name"]
        assert "id" in data

    async def test_update_area(self, app_client: AsyncClient):
        # given

        # when
        update_data = {
            "name": "Updated Area",
            "address": "789 Updated St",
            "website": "http://updated.com",
            "contact_num": "111-222-3333",
            "open_time": "8:00 AM - 4:00 PM",
        }
        response = await app_client.put(
            f"kbuddy/api/v1/area/{self.area_id}",
            json=update_data,
        )

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["address"] == update_data["address"]

    async def test_delete_area(self, app_client: AsyncClient):
        # given

        # when
        response = await app_client.delete(f"kbuddy/api/v1/area/{self.area_id}")

        # then
        assert response.status_code == 204

    async def test_create_area_image(self, app_client: AsyncClient):
        # given
        image_data = {
            "area_img": "http://test.com/image.jpg",
            "created_at": "2023-01-01T00:00:00",
        }

        # when
        response = await app_client.post(
            f"kbuddy/api/v1/area/{self.area_id}/images", json=image_data
        )

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["area_img"] == image_data["area_img"]
        assert "id" in data

    async def test_get_area_images(self, app_client: AsyncClient):
        # given
        response = await app_client.get(f"kbuddy/api/v1/area/{self.area_id}/images")
        assert response.status_code == 200
        assert len(response.json()) == 0  # before check

        for i in range(5):
            image_data = {
                "area_img": f"http://test.com/image{i}.jpg",
                "created_at": "2023-01-01T00:00:00",
            }
            await app_client.post(
                f"kbuddy/api/v1/area/{self.area_id}/images", json=image_data
            )

        # when
        response = await app_client.get(f"kbuddy/api/v1/area/{self.area_id}/images")

        # then
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["area_img"] == "http://test.com/image0.jpg"
        assert data[0]["area_id"] == 1

    async def test_get_area_image(self, app_client: AsyncClient):
        # given
        image_data = {
            "area_img": "http://test.com/image.jpg",
            "created_at": "2023-01-01T00:00:00",
        }
        response = await app_client.post(
            f"kbuddy/api/v1/area/{self.area_id}/images", json=image_data
        )
        image_id = response.json()["id"]

        # when
        response = await app_client.get(f"kbuddy/api/v1/area/images/{image_id}")

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["area_img"] == image_data["area_img"]
        assert "id" in data

    async def test_update_area_image(self, app_client: AsyncClient):
        # given
        image_data = {
            "area_img": "http://test.com/image.jpg",
            "created_at": "2023-01-01T00:00:00",
        }
        response = await app_client.post(
            f"kbuddy/api/v1/area/{self.area_id}/images", json=image_data
        )
        image_id = response.json()["id"]

        # when
        update_data = {
            "area_img": "http://updated.com/updated_image.jpg",
            "created_at": "2023-02-02T00:00:00",
        }
        response = await app_client.put(
            f"kbuddy/api/v1/area/images/{image_id}",
            json=update_data,
        )

        # then
        assert response.status_code == 200
        data = response.json()
        assert data["area_img"] == update_data["area_img"]
        assert data["created_at"] == update_data["created_at"]

    async def test_delete_area_image(self, app_client: AsyncClient):
        # given
        image_data = {
            "area_img": "http://test.com/image.jpg",
            "created_at": "2023-01-01T00:00:00",
        }
        response = await app_client.post(
            f"kbuddy/api/v1/area/{self.area_id}/images", json=image_data
        )
        image_id = response.json()["id"]

        # when
        response = await app_client.delete(f"kbuddy/api/v1/area/images/{image_id}")

        # then
        assert response.status_code == 204
