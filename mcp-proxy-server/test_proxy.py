import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_unknown_target():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/unknown/invoke_method", json={"method": "foo", "params": {}})
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_aggregate_methods():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/aggregate_methods")
        assert response.status_code == 200
        assert "methods" in response.json()

import httpx

def test_invoke(target="github", method="list_issues", params=None):
    if params is None:
        params = {}
    url = f"http://localhost:9000/{target}/invoke_method"
    payload = {"method": method, "params": params}
    response = httpx.post(url, json=payload)
    return response.json()

if __name__ == "__main__":
    print(test_invoke())
