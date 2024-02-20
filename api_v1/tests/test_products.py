import pytest

from core.settings import settings


class TestProducts:
    url = f"{settings.api_v1_prefix}/products"

    def test_get_products(self, client):
        response = client.get(self.url)
        assert response.status_code == 200
        # assert response.json() == []
