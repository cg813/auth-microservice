import pytest


@pytest.mark.asyncio
async def test_sing_in_with_email_which_does_not_exists(client):
    res = await client.post("/api/users/login", json={"email": "test@test.com", "password": "testPassword"})
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_sign_in_with_incorrect_password(client):
    await client.post("/api/users/signup", json={"email": "test@test.com", "password": "testPassword"})

    res = await client.post('/api/users/login', json={"email": "test@test.com", "password": "test123"})

    assert res.status_code == 401


@pytest.mark.asyncio
async def test_sign_in_with_correct_credentials(client):
    await client.post("/api/users/signup", json={"email": "test@test.com", "password": "testPassword"})

    res = await client.post('/api/users/login', json={"email": "test@test.com", "password": "testPassword"})
    response_data = res.json()
    assert res.status_code == 200

    assert "id" in response_data
    assert "email" in response_data
    assert res.headers.get("set-cookie") is not None
