import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_integrate_data_valid_source():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/data/integrate", json={"source": "GSA_CALC"})
    assert response.status_code == 202
    assert response.json() == {"status": "ETL started", "detail": "GSA_CALC ETL initiated."}

@pytest.mark.asyncio
async def test_integrate_data_invalid_source():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/data/integrate", json={"source": "INVALID_SOURCE"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid data source."}
