import pytest


@pytest.mark.asyncio
async def test_sign_up_route(client):
    res = await client.post('/api/users/signup', json={"email": "test@test.com",
                                                       "password": "testPassword12"})
    response_data = res.json()
    assert res.status_code == 201
    assert 'id' in response_data
    assert response_data['email'] == 'test@test.com'


@pytest.mark.asyncio
async def test_sign_up_route_with_invalid_email(client):
    res = await client.post('/api/users/signup', json={"email": "test", "password": "testPassword12"})
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_sign_up_route_with_invalid_password(client):
    res = await client.post('/api/users/signup', json={"email": "test@test.com", "password": "te"})
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_sign_up_route_with_missing_fields(client):
    res = await client.post("/api/users/signup", json={})
    assert res.status_code == 422

    res = await client.post("/api/users/signup", json={"email": "test@test.com"})
    assert res.status_code == 422

    res = await client.post("/api/users/signup", json={"password": "testPassword"})
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_disallow_duplicated_emails(client):
    res = await client.post('/api/users/signup', json={"email": "test@test.com",
                                                       "password": "testPassword12"})
    assert res.status_code == 201

    res = await client.post('/api/users/signup', json={"email": "test@test.com",
                                                       "password": "testPassword12"})
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_cookie_after_successful_sing_up(client):
    res = await client.post('/api/users/signup', json={"email": "test@test.com",
                                                       "password": "testPassword12"})
    assert res.status_code == 201
    assert res.headers.get('set-cookie') is not None
