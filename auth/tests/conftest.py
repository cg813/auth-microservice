import os
import asyncio
import pytest
import motor.motor_asyncio

from httpx import AsyncClient
from starlette.testclient import TestClient
from beanie import init_beanie

from main import app
from src.config import Settings, get_settings
from src.documents import User


def get_settings_override():
    return Settings(testing=1, DATABASE_NAME="test", MONGODB_URL=os.environ.get("AUTH_MONGODB_URL"))


@pytest.fixture(scope="module")
def test_app():
    # set up
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="session", autouse=True)
async def project_setup():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("AUTH_MONGODB_URL"))
    await init_beanie(
        database=client["test_users"],
        document_models=[User],
    )


@pytest.fixture(autouse=True)
async def tear_down():
    await User.get_motor_collection().drop()


@pytest.fixture()
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://localhost:8001") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
