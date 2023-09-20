import pytest


@pytest.mark.asyncio
async def test_ping(client):
    response = await client.get("/health")
    assert response.status_code == 200

