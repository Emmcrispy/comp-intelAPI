import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_generate_report_valid_id():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/reports/compensation_summary")
    assert response.status_code == 200
    assert response.json() == {
        "report": "Compensation Analysis",
        "content": "Report Data..."
    }

@pytest.mark.asyncio
async def test_generate_report_invalid_id():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/reports/nonexistent_report")
    assert response.status_code == 404
    assert response.json() == {"detail": "Report not found."}
