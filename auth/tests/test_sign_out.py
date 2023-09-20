import pytest


@pytest.mark.asyncio
async def test_log_out_clears_cookie(client):
    res = await client.post("/api/users/signup", json={"email": "test@test.com", "password": "testPassword"})
    assert res.status_code == 201

    res = await client.post("/api/users/sign/out")
    assert res.status_code == 200
