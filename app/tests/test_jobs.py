import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_upload_job():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/jobs/upload", json={"description": "Analyst needed"})
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_search_jobs():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/jobs/search?keyword=analyst")
    assert response.status_code == 200
